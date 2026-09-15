<script setup>
import { ref, watch } from 'vue'
import { Printer, Download } from '@element-plus/icons-vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  title: { type: String, default: '' },
})

const emit = defineEmits(['update:visible'])

const dialogVisible = ref(false)

watch(() => props.visible, (val) => {
  dialogVisible.value = val
})

watch(dialogVisible, (val) => {
  if (!val) emit('update:visible', false)
})

function handlePrint() {
  window.print()
}

function handleExportPdf() {
  window.print()
}

function handleClose() {
  dialogVisible.value = false
}
</script>

<template>
  <el-dialog
    v-model="dialogVisible"
    :title="title"
    width="90%"
    top="5vh"
    :close-on-click-modal="false"
    :destroy-on-close="true"
    class="print-preview-dialog"
  >
    <div class="print-content">
      <slot />
    </div>

    <template #footer>
      <div class="print-preview-footer no-print">
        <el-button type="primary" :icon="Printer" @click="handlePrint">打印</el-button>
        <el-button type="success" :icon="Download" @click="handleExportPdf">导出PDF</el-button>
        <el-button @click="handleClose">关闭</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style scoped>
.print-preview-dialog :deep(.el-dialog__body) {
  padding: 0;
  max-height: 70vh;
  overflow-y: auto;
}

.print-content {
  padding: 0;
}

.print-preview-footer {
  display: flex;
  justify-content: center;
  gap: 12px;
}

@media print {
  html, body {
    margin: 0 !important;
    padding: 0 !important;
    background: #fff !important;
  }

  .no-print,
  .print-preview-dialog :deep(.el-dialog__header),
  .print-preview-dialog :deep(.el-dialog__footer),
  .print-preview-dialog :deep(.el-overlay),
  .print-preview-dialog :deep(.el-overlay-dialog) {
    display: none !important;
  }

  .print-preview-dialog :deep(.el-dialog) {
    position: static !important;
    width: 100% !important;
    max-width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    box-shadow: none !important;
    border: none !important;
    background: #fff !important;
    border-radius: 0 !important;
  }

  .print-preview-dialog :deep(.el-dialog__body) {
    max-height: none !important;
    overflow: visible !important;
    padding: 0 !important;
  }
}
</style>

<style>
@media print {
  @page {
    size: A4;
    margin: 0;
  }

  .el-overlay,
  .el-overlay-dialog,
  .el-dialog__wrapper,
  .el-overlay-mask {
    display: none !important;
  }

  html, body, #app, .el-dialog, .el-dialog__body, .el-dialog__wrapper {
    background: #fff !important;
    box-shadow: none !important;
    border: none !important;
    outline: none !important;
  }
}
</style>