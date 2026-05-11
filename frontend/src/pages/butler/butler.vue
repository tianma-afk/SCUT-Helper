<template>
  <view class="page">
    <view class="chat-container">
      <view class="chat-card">
        <view class="chat-message user-message">
          今天食堂有什么特色推荐菜？
        </view>
        <view class="chat-message bot-message">
          <view class="avatar">
            <text class="icon">💬</text>
          </view>
          <view class="content">
            <view class="text-line">为您找到今日食堂的特色推荐菜品：</view>
            <view class="food-item">🍲 红烧肉 (一饭二楼)</view>
            <view class="food-item">🐟 姜葱蒸鱼 (二饭一楼)</view>
            <view class="food-item">🌶️ 麻婆豆腐 (三饭二楼)</view>
            <view class="text-line highlight">建议避开12:00-12:30的高峰期前往就餐哦！</view>
          </view>
        </view>
      </view>
      
      <view class="pagination-dots">
        <view class="dot"></view>
        <view class="dot active"></view>
        <view class="dot"></view>
      </view>
    </view>

    <TabBar :current="1" />
  </view>
</template>

<script setup>
import TabBar from '@/components/TabBar.vue'
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #f8f9fc;
  padding: 60rpx 40rpx 180rpx;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.chat-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  flex: 1;
}

.chat-card {
  background: #ffffff;
  border-radius: 32rpx;
  padding: 40rpx 30rpx;
  box-shadow: 0 10rpx 30rpx rgba(0, 0, 0, 0.08);
  width: 92%;
  max-width: 680rpx;
  box-sizing: border-box;
  margin-bottom: 40rpx;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.user-message {
  background-color: #3b82f6;
  color: #ffffff;
  padding: 24rpx 32rpx;
  border-radius: 20rpx;
  font-size: 28rpx;
  margin-bottom: 40rpx;
  align-self: flex-end;
  max-width: 85%;
  border-bottom-right-radius: 4rpx;
}

.bot-message {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  background-color: #f8f9fc;
  padding: 32rpx;
  border-radius: 20rpx;
  align-self: flex-start;
  width: 100%;
  box-sizing: border-box;
  
  .avatar {
    background-color: #e0f2fe;
    width: 64rpx;
    height: 64rpx;
    border-radius: 32rpx;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-right: 24rpx;
    flex-shrink: 0;
    
    .icon {
      font-size: 32rpx;
      color: #3b82f6;
    }
  }
  
  .content {
    flex: 1;
    font-size: 28rpx;
    color: #333333;
    line-height: 1.6;
    
    .text-line {
      margin-bottom: 16rpx;
    }
    
    .highlight {
      margin-top: 24rpx;
      color: #4a5568;
    }
    
    .food-item {
      margin-bottom: 8rpx;
      padding-left: 12rpx;
    }
  }
}

.pagination-dots {
  display: flex;
  gap: 12rpx;
  
  .dot {
    width: 12rpx;
    height: 12rpx;
    background-color: #cbd5e1;
    border-radius: 6rpx;
    
    &.active {
      width: 32rpx;
      background-color: #3b82f6;
    }
  }
}
</style>