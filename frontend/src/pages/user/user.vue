<template>
  <view class="page">
    <view class="header-bg"></view>
    
    <view class="content">
      <!-- 用户信息卡片 -->
      <view class="profile-card">
        <view class="avatar">
          <svg viewBox="0 0 24 24" fill="none" stroke="#94a3b8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 64rpx; height: 64rpx;">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
            <circle cx="12" cy="7" r="4"></circle>
          </svg>
        </view>
        <view class="info">
          <view class="name">张三</view>
          <view class="tags">
            <text class="tag-badge">本科生</text>
            <text class="tag-desc">计算机科学与技术</text>
          </view>
        </view>
      </view>

      <!-- 数据统计面板 -->
      <view class="stats-panel">
        <view class="stat-item">
          <view class="number">128</view>
          <view class="label">完成任务</view>
        </view>
        <view class="divider"></view>
        <view class="stat-item">
          <view class="number">45</view>
          <view class="label">活跃天数</view>
        </view>
        <view class="divider"></view>
        <view class="stat-item">
          <view class="number">12</view>
          <view class="label">使用助手</view>
        </view>
      </view>

      <!-- 功能列表 -->
      <view class="menu-list">
        <view class="menu-item" @tap="handleFeedback">
          <view class="menu-left">
            <view class="menu-icon warning">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 40rpx; height: 40rpx;">
                <path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"></path>
              </svg>
            </view>
            <text class="menu-text">我的收藏</text>
          </view>
          <view class="menu-right">></view>
        </view>
        <view class="menu-item" @tap="openBlog">
          <view class="menu-left">
            <view class="menu-icon settings">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 40rpx; height: 40rpx;">
                <circle cx="12" cy="12" r="3"></circle>
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
              </svg>
            </view>
            <text class="menu-text">设置</text>
          </view>
          <view class="menu-right">></view>
        </view>
        <view class="menu-item" @tap="handleFeedback">
          <view class="menu-left">
            <view class="menu-icon help">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 40rpx; height: 40rpx;">
                <circle cx="12" cy="12" r="10"></circle>
                <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
            </view>
            <text class="menu-text">帮助与反馈</text>
          </view>
          <view class="menu-right">></view>
        </view>
      </view>

      <!-- 退出登录 -->
      <view class="logout-btn" @tap="switchToLogin">
        <view class="logout-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="#64748b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width: 44rpx; height: 44rpx;">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
            <polyline points="16 17 21 12 16 7"></polyline>
            <line x1="21" y1="12" x2="9" y2="12"></line>
          </svg>
        </view>
        <text>退出登录</text>
      </view>
    </view>
    
    <!-- 底部导航栏 -->
    <TabBar :current="2" />
  </view>
</template>

<script setup>
import { onMounted } from 'vue'
import TabBar from '@/components/TabBar.vue'

const switchToLogin = () => {
  try {
    uni.reLaunch({
      url: '../login/login'
    })
  } catch (err) {
    console.error('跳转失败', err)
  }
}

const openBlog = () => {
  const blogUrl = 'https://moon-explorer.top'
  uni.setClipboardData({
    data: blogUrl
  })
}

const handleFeedback = () => {
  const feedbackUrl = 'https://dcnmcid6v0ct.feishu.cn/wiki/RFEbw4pV8iP6IUkiAzMcmBwKn7c'
  uni.setClipboardData({
    data: feedbackUrl
  })
}
</script>

<style lang="scss" scoped>
.page {
  min-height: 100vh;
  background-color: #f8f9fc;
  padding-bottom: 160rpx;
  position: relative;
}

.header-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 360rpx;
  background: linear-gradient(135deg, #4f8bf9 0%, #356be6 100%);
  border-bottom-left-radius: 60rpx;
  border-bottom-right-radius: 60rpx;
  z-index: 0;
}

.content {
  position: relative;
  z-index: 1;
  padding: 100rpx 40rpx 40rpx;
}

.profile-card {
  background: #ffffff;
  border-radius: 32rpx;
  padding: 40rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.05);
  margin-bottom: 40rpx;

  .avatar {
    width: 120rpx;
    height: 120rpx;
    background-color: #f0f4fd;
    border-radius: 60rpx;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 60rpx;
    margin-right: 32rpx;
    color: #999;
  }

  .info {
    .name {
      font-size: 44rpx;
      font-weight: bold;
      color: #333;
      margin-bottom: 12rpx;
    }

    .tags {
      display: flex;
      align-items: center;

      .tag-badge {
        background-color: #e6f0ff;
        color: #3b82f6;
        font-size: 20rpx;
        padding: 4rpx 16rpx;
        border-radius: 16rpx;
        margin-right: 16rpx;
      }

      .tag-desc {
        color: #888;
        font-size: 24rpx;
      }
    }
  }
}

.stats-panel {
  background: #ffffff;
  border-radius: 32rpx;
  padding: 40rpx 0;
  display: flex;
  justify-content: space-evenly;
  align-items: center;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.05);
  margin-bottom: 40rpx;

  .stat-item {
    display: flex;
    flex-direction: column;
    align-items: center;

    .number {
      font-size: 40rpx;
      font-weight: bold;
      color: #222;
      margin-bottom: 8rpx;
    }

    .label {
      font-size: 24rpx;
      color: #888;
    }
  }

  .divider {
    width: 2rpx;
    height: 60rpx;
    background-color: #f0f0f0;
  }
}

.menu-list {
  background: #ffffff;
  border-radius: 32rpx;
  padding: 16rpx 40rpx;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.05);
  margin-bottom: 40rpx;

  .menu-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 32rpx 0;
    border-bottom: 2rpx solid #f8f8f8;

    &:last-child {
      border-bottom: none;
    }

    .menu-left {
      display: flex;
      align-items: center;

      .menu-icon {
        display: flex;
        align-items: center;
        margin-right: 24rpx;
        
        &.warning { color: #ea580c; } /* 橙褐色 */
        &.settings { color: #64748b; } /* 灰色 */
        &.help { color: #3b82f6; } /* 蓝色 */
      }

      .menu-text {
        font-size: 30rpx;
        color: #333;
        font-weight: 500;
      }
    }

    .menu-right {
      color: #cbd5e1;
      font-size: 32rpx;
      font-weight: 300;
    }
  }
}

.logout-btn {
  background: #ffffff;
  border-radius: 32rpx;
  padding: 32rpx;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 10rpx 40rpx rgba(0, 0, 0, 0.05);
  color: #475569;
  font-size: 32rpx;
  font-weight: 600;

  .logout-icon {
    display: flex;
    align-items: center;
    margin-right: 16rpx;
  }
}
</style>