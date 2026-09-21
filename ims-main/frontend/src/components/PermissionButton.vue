<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  /** 权限键，如 "inbound.create" */
  permKey: { type: String, required: true },
  /** 无权限时的提示文本 */
  tip: { type: String, default: '' },
})

const auth = useAuthStore()
const canEdit = computed(() => auth.canEdit(props.permKey))
const tooltipText = computed(() => props.tip || '当前角色无此操作权限')
</script>

<template>
  <el-tooltip
    v-if="!canEdit"
    :content="tooltipText"
    placement="top"
    :show-after="200"
  >
    <span class="permission-btn--disabled">
      <slot />
    </span>
  </el-tooltip>
  <slot v-else />
</template>

<style scoped>
.permission-btn--disabled {
  cursor: not-allowed;
  display: inline-flex;
}
.permission-btn--disabled :deep(.el-button),
.permission-btn--disabled :deep(.el-link) {
  pointer-events: none;
  opacity: 0.45;
}
</style>