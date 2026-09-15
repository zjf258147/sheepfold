import { describe, it, expect, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { defineComponent, ref } from 'vue'

const Counter = defineComponent({
  template: '<div><span class="count">{{ count }}</span><button class="add" @click="count++">+</button><button class="reset" @click="count = 0">Reset</button></div>',
  setup() {
    const count = ref(0)
    return { count }
  },
})

const Message = defineComponent({
  props: { title: String, content: String },
  template: '<div class="message"><h2>{{ title }}</h2><p>{{ content }}</p><slot /></div>',
})

describe('Vue组件测试', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  describe('Counter组件', () => {
    it('渲染组件', () => {
      const wrapper = mount(Counter)
      expect(wrapper.exists()).toBe(true)
    })

    it('初始值为0', () => {
      const wrapper = mount(Counter)
      expect(wrapper.find('.count').text()).toBe('0')
    })

    it('点击递增', async () => {
      const wrapper = mount(Counter)
      await wrapper.find('.add').trigger('click')
      expect(wrapper.find('.count').text()).toBe('1')
    })

    it('多次点击正确累加', async () => {
      const wrapper = mount(Counter)
      const btn = wrapper.find('.add')
      for (let i = 0; i < 5; i++) {
        await btn.trigger('click')
      }
      expect(wrapper.find('.count').text()).toBe('5')
    })

    it('Reset重置为0', async () => {
      const wrapper = mount(Counter)
      await wrapper.find('.add').trigger('click')
      await wrapper.find('.add').trigger('click')
      expect(wrapper.find('.count').text()).toBe('2')
      await wrapper.find('.reset').trigger('click')
      expect(wrapper.find('.count').text()).toBe('0')
    })
  })

  describe('Message组件', () => {
    it('渲染props', () => {
      const wrapper = mount(Message, {
        props: { title: '测试标题', content: '测试内容' },
      })
      expect(wrapper.find('h2').text()).toBe('测试标题')
      expect(wrapper.find('p').text()).toBe('测试内容')
    })

    it('渲染slot', () => {
      const wrapper = mount(Message, {
        props: { title: '标题', content: '内容' },
        slots: { default: '<span class="extra">额外内容</span>' },
      })
      expect(wrapper.find('.extra').text()).toBe('额外内容')
    })

    it('响应式更新props', async () => {
      const wrapper = mount(Message, {
        props: { title: '旧标题', content: '旧内容' },
      })
      await wrapper.setProps({ title: '新标题' })
      expect(wrapper.find('h2').text()).toBe('新标题')
    })
  })
})