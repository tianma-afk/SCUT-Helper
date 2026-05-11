<template>
  <view class="custom-tab-bar">
    <view 
      class="tab-item" 
      :class="{ active: current === 0 }"
      @tap="switchTab(0, '/pages/index/index')"
    >
      <view class="tab-icon-wrapper">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="2" y1="12" x2="22" y2="12"></line>
          <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path>
        </svg>
      </view>
      <view class="tab-text">世界</view>
    </view>
    <view 
      class="tab-item" 
      :class="{ active: current === 1 }"
      @tap="switchTab(1, '/pages/butler/butler')"
    >
      <view class="tab-icon-wrapper">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
        </svg>
      </view>
      <view class="tab-text">管家</view>
    </view>
    <view 
      class="tab-item" 
      :class="{ active: current === 2 }"
      @tap="switchTab(2, '/pages/user/user')"
    >
      <view class="tab-icon-wrapper">
        <svg class="tab-svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </view>
      <view class="tab-text">我的</view>
    </view>
  </view>
</template>

<script setup>
const props = defineProps({
  current: {
    type: Number,
    default: 0
  }
})

const switchTab = (index, path) => {
  if (props.current !== index) {
    try {
      uni.reLaunch({
        url: path
      })
    } catch (err) {
      console.error('跳转失败', err)
    }
  }
}
</script>

<style lang="scss" scoped>
.custom-tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 140rpx;
  background: #ffffff;
  display: flex;
  justify-content: space-around;
  align-items: center;
  border-top: 1px solid #f1f5f9;
  z-index: 999;
  padding-bottom: env(safe-area-inset-bottom);
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  padding: 8rpx 0;
  color: #94a3b8; /* 未选中时的灰色 */
  transition: color 0.3s ease;
}

.tab-item.active {
  color: #3b82f6; /* 选中时的蓝色 */
  
  .tab-icon-wrapper {
    background-color: #eff6ff; /* 浅蓝色背景 */
  }
}

.tab-icon-wrapper {
  width: 100rpx;
  height: 100rpx;
  border-radius: 32rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 4rpx;
  transition: background-color 0.3s ease;
}

.tab-svg {
  width: 52rpx;
  height: 52rpx;
}

.tab-text {
  font-size: 24rpx;
  font-weight: 500;
  margin-top: -8rpx;
}
</style>