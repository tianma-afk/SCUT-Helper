<template>
  <view class="page">
    <view class="welcome-screen" v-if="messages.length === 0">
      <text class="welcome-text">小主人你好啊！</text>
    </view>

    <scroll-view 
      v-else
      class="chat-scroll" 
      scroll-y 
      :scroll-into-view="scrollTarget" 
      :scroll-with-animation="true"
    >
      <view class="chat-padding-top"></view>
      <view 
        v-for="(msg, index) in messages" 
        :key="index" 
        :id="'msg-' + index"
        class="chat-message-wrapper"
        :class="msg.role"
      >
        <view class="message-content" :class="{'user-message': msg.role === 'user', 'bot-message': msg.role === 'bot'}">
          <text class="text-content">{{ msg.content }}</text>
          <view v-if="msg.role === 'bot' && !msg.content && isLoading && index === messages.length - 1" class="typing-indicator">
            <text class="dot">.</text><text class="dot">.</text><text class="dot">.</text>
          </view>
        </view>
      </view>
      <view class="chat-padding-bottom"></view>
    </scroll-view>

    <!-- 底部输入区域 -->
    <view class="input-area">
      <input 
        class="msg-input" 
        v-model="inputText" 
        placeholder="发送消息给智能管家..." 
        confirm-type="send"
        @confirm="sendMessage" 
      />
      <button class="send-btn" :class="{ disabled: isLoading || !inputText.trim() }" @tap="sendMessage">
        发送
      </button>
    </view>

    <TabBar :current="1" />
  </view>
</template>

<script setup>
import { ref } from 'vue'
import TabBar from '@/components/TabBar.vue'

const messages = ref([])
const inputText = ref('')
const isLoading = ref(false)
const scrollTarget = ref('')

const sendMessage = () => {
  const text = inputText.value.trim()
  if (!text || isLoading.value) return

  // 展示用户消息
  messages.value.push({ role: 'user', content: text })
  inputText.value = ''
  
  // 占位机器人回复
  messages.value.push({ role: 'bot', content: '' })
  const botIdx = messages.value.length - 1
  isLoading.value = true
  scrollToBottom(botIdx)

  // 模拟请求后端的流式/chat/stream接口
  // 由于uniapp环境中支持enableChunked
  const requestTask = uni.request({
    url: `http://localhost:8443/api/v1/chat/stream?message=${encodeURIComponent(text)}`,
    method: 'POST',
    enableChunked: true,
    success: (res) => {
      // 请求成功完毕
      isLoading.value = false
    },
    fail: (err) => {
      messages.value[botIdx].content = '网络请求失败，请稍后重试。'
      isLoading.value = false
    }
  })

  let buffer = ''
  requestTask.onChunkReceived && requestTask.onChunkReceived((res) => {
    // 兼容 ArrayBuffer (小程序) 或 Base64 (视环境而定)
    let chunkText = ''
    try {
      const uint8Arr = new Uint8Array(res.data)
      // 如果支持 TextDecoder (H5/部分小程序基础库)
      if (typeof TextDecoder !== 'undefined') {
        chunkText = new TextDecoder('utf-8').decode(uint8Arr)
      } else {
        // Fallback for some basic environments without TextDecoder
        let str = ''
        for (let i = 0; i < uint8Arr.length; i++) {
          str += String.fromCharCode(uint8Arr[i])
        }
        chunkText = decodeURIComponent(escape(str))
      }
    } catch (e) {
      console.error('解码失败', e)
    }

    buffer += chunkText
    let start = 0
    for (let i = 0; i < buffer.length; i++) {
      if (buffer[i] === '}') {
        const potentialJson = buffer.substring(start, i + 1)
        try {
          const data = JSON.parse(potentialJson)
          start = i + 1
          
          if (data.type === 'chunk') {
            messages.value[botIdx].content += data.data
          } else if (data.type === 'end') {
            isLoading.value = false
          }
          scrollToBottom(botIdx)
        } catch (e) {
          // not valid json yet, proceed
        }
      }
    }
    buffer = buffer.substring(start)
  })
}

const scrollToBottom = (idx) => {
  setTimeout(() => {
    scrollTarget.value = 'msg-' + idx
  }, 50) 
}
</script>

<style lang="scss" scoped>
.page {
  height: 100vh;
  background-color: #f8f9fc;
  display: flex;
  flex-direction: column;
  position: relative;
}

.welcome-screen {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.welcome-text {
  font-size: 40rpx;
  color: #3b82f6;
  font-weight: bold;
  opacity: 0.9;
}

.chat-scroll {
  flex: 1;
  height: 0; // 为了让scroll-view生效，必须限制高度
  width: 100%;
}

.chat-padding-top {
  height: 40rpx;
}

.chat-padding-bottom {
  // 底部留出输入框和TabBar的空间
  height: calc(140rpx + 160rpx + 60rpx);
}

.chat-message-wrapper {
  display: flex;
  width: 100%;
  padding: 20rpx 40rpx;
  box-sizing: border-box;

  &.user {
    justify-content: flex-end;
  }
  &.bot {
    justify-content: flex-start;
  }
}

.message-content {
  max-width: 75%;
  font-size: 28rpx;
  line-height: 1.6;
  word-wrap: break-word;
  word-break: break-all;
  white-space: pre-wrap;
  
  .text-content {
    display: inline-block;
  }
}

.user-message {
  background-color: #3b82f6;
  color: #ffffff;
  padding: 20rpx 32rpx;
  border-radius: 20rpx;
  border-bottom-right-radius: 4rpx;
}

.bot-message {
  background-color: #ffffff;
  color: #333333;
  padding: 20rpx 32rpx;
  border-radius: 20rpx;
  border-bottom-left-radius: 4rpx;
  box-shadow: 0 4rpx 16rpx rgba(0, 0, 0, 0.04);
}

.input-area {
  position: fixed;
  bottom: 140rpx; /* TabBar 的高度 */
  left: 0;
  right: 0;
  background-color: #ffffff;
  padding: 24rpx 30rpx;
  display: flex;
  align-items: center;
  border-top: 1px solid #f1f5f9;
  z-index: 100;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  
  .msg-input {
    flex: 1;
    background-color: #f1f5f9;
    height: 76rpx;
    border-radius: 38rpx;
    padding: 0 32rpx;
    font-size: 28rpx;
    margin-right: 20rpx;
  }
  
  .send-btn {
    background-color: #3b82f6;
    color: #fff;
    height: 76rpx;
    line-height: 76rpx;
    border-radius: 38rpx;
    font-size: 28rpx;
    padding: 0 40rpx;
    margin: 0;
    
    &.disabled {
      background-color: #94a3b8;
    }
  }
}

.typing-indicator {
  display: inline-block;
  margin-left: 8rpx;
  .dot {
    animation: typing 1.4s infinite;
    display: inline-block;
    &:nth-child(2) { animation-delay: 0.2s; }
    &:nth-child(3) { animation-delay: 0.4s; }
  }
}

@keyframes typing {
  0%, 100% { opacity: 0.2; }
  50% { opacity: 1; }
}
</style>