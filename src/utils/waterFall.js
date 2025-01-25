import { ref } from 'vue'

export class WaterFall {
  constructor(columns, card_columns, cards) {
    this.columns = columns
    this.card_columns = card_columns
    this.arrHeight = ref([])
    this.cards = cards
  }
  // 初始化瀑布流布局
  init() {
    this.card_columns.value = {}
    this.arrHeight.value = []
    // 初始化列
    this.card_columns.value = Array.from({ length: this.columns.value }, () => [])
    // 分配卡片到最短的列
    for (let i = 0; i < this.cards.value.length; i++) {
      const height = this._calculateCardHeight(this.cards.value[i])

      if (i < this.columns.value) {
        this.card_columns.value[i].push(this.cards.value[i])
        this.arrHeight.value.push(height)
      } else {
        const { minI } = this._findShortestColumn()
        this.card_columns.value[minI].push(this.cards.value[i])
        this.arrHeight.value[minI] += height
      }
    }
  }

  // 加载更多卡片
  loadMore(more) {
    for (let i = 0; i < more.length; i++) {
      const height = this._calculateCardHeight(more[i])
      const { minI } = this._findShortestColumn()

      this.card_columns.value[minI].push(more[i])
      this.arrHeight.value[minI] += height
    }
  }

  calculate(contentWidth) {
    const width = Math.floor(contentWidth / 280)
    this.columns.value = width > 1 ? width : 1 // 最少一列
  }

  // 计算卡片高度
  _calculateCardHeight(card) {
    return card.img_info.height / (card.img_info.width / 250)
  }

  // 找到最短的列
  _findShortestColumn() {
    const { minH, minI } = this.arrHeight.value.reduce(
        (acc, val, index) =>
            (val < acc.minH ? { minH: val, minI: index } : acc),
        { minH: Infinity, minI: 0 }
    );
    return {minH,minI}
  }
}
