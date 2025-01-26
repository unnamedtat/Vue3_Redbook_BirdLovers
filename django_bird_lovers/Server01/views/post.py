import json

from PIL import Image
from django.db.models import Q
from django.http import JsonResponse

import Server01.models as models
from Server01.util.auxiliaryFuction import convert_to_timezone, combine_index_post, filter_querySet, post_to_picgo
from Server01.util.verifyJWT import authenticate_request
from webServer.settings import TIME_ZONE, STATIC_IMG_PATH


@authenticate_request
def upload_post(request, payload):
    files = request.FILES.getlist('files[]')
    post_id = request.POST.get('id')
    post = models.Post.objects.filter(id=post_id).first()
    if not post:
        return JsonResponse({'error': '投稿失败'}, status=404)
    # 初始化上传结果列表
    upload_results = []
    # 遍历所有文件并逐个上传和保存
    for file in files:
        img_uuid_seed = f'{post_id}-{file.name}'
        upload_result = post_to_picgo(file, img_uuid_seed, post_type='post')

        # 创建 Image 实例（初始占位数据）
        image = models.Image.objects.create(
            imagePath='',
            deleteUrl='',
            post=post,
            height=300,
            width=250
        )

        # 检查上传结果
        if upload_result['status'] == 'success':
            # 保存上传成功的文件路径和其他信息
            image.imagePath = upload_result['url']
            image.deleteUrl = upload_result['delete_url']
            image.height = upload_result['height']
            image.width = upload_result['width']
            image.save()

            upload_results.append({
                'file': file.name,
                'status': 'success',
                'url': upload_result['url']
            })
        else:
            # 如果某个文件上传失败，记录错误信息
            upload_results.append({
                'file': file.name,
                'status': 'error',
                'message': '图片上传错误'
            })
    return JsonResponse({'info': upload_results}, status=200)


# 用户上传帖子
@authenticate_request
def upload_post_info(request, payload):
    data = json.loads(request.body)
    post = models.Post.objects.create(
        title=data.get('title'),
        content=data.get('content'),
        user_id=data.get('user_id')
    )
    return JsonResponse({'data': 'success', 'info': post.id}, status=200)


# 获取帖子详情，整合信息
def get_post_detail(request):
    data = json.loads(request.body)
    id = data.get('id')
    post = models.Post.objects.filter(id=id).first()
    if post:
        imgs = post.imgs.all()
        info = {
            'title': post.title,            'id': post.id,
            'imgs': [img.imagePath for img in imgs],
            'user': {
                'id': post.user.id,
                'username': post.user.username,
                'avatar': post.user.avatar
            },
            'createTime': convert_to_timezone(post.created_at, TIME_ZONE),
            'likeCount': post.favoritePosts.count(),
            'collectCount': post.collectedPosts.count(),
            'commentCount': post.comments.count(),
            'content': post.content
        }
        return JsonResponse({'info': info}, status=200)
    return JsonResponse({'error': '错误的访问'}, status=404)


# 主页推送帖子
def query_post_index(request):
    data = json.loads(request.body)
    offset = data['offset']
    query = data.get('query')
    if query:
        posts = models.Post.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(content__icontains=query)
        )
    else:
        posts = models.Post.objects
    posts = filter_querySet(posts, offset, limit=10)
    if posts:
        return JsonResponse({'info': list(combine_index_post(posts))}, status=200)
    # 没有内容了
    return JsonResponse({'info': []}, status=200)


@authenticate_request
def control_like_collect(request, payload):
    user_id = payload['user_id']
    data = json.loads(request.body)
    operation = data['operator']
    post_id = data['post_id']
    types = data['type']
    user = models.User.objects.filter(id=user_id).first()
    post = models.Post.objects.filter(id=post_id).first()
    if user and post:
        if types == 'like':
            if not operation:
                user.favorites.add(post)
                return JsonResponse({'info': '成功添加喜欢'}, status=200)
            user.favorites.remove(post)
            return JsonResponse({'info': '成功取消喜欢'}, status=200)
        elif types == 'collect':
            if not operation:
                user.collected.add(post)
                return JsonResponse({'info': '成功添加收藏'}, status=200)
            user.collected.remove(post)
            return JsonResponse({'info': '成功取消收藏'}, status=200)
    return JsonResponse({'error': '错误的操作'}, status=404)


@authenticate_request
def post_delete(request, payload):
    data = json.loads(request.body)
    id = data['id']
    post = models.Post.objects.filter(id=id).first()
    if post:
        if post.user.id == payload['user_id']:
            post.delete()
            return JsonResponse({'success': '帖子删除成功'}, status=200)
        return JsonResponse({'error': '错误'}, status=401)
    return JsonResponse({'error': '错误'}, status=401)