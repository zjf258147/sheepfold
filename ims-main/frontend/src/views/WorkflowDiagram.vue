<script setup>
import { onMounted, ref, nextTick, onUnmounted } from 'vue'
import mermaid from 'mermaid'
import { ZoomIn, ZoomOut } from '@element-plus/icons-vue'

mermaid.initialize({
  startOnLoad: false,
  theme: 'base',
  themeVariables: {
    primaryColor: '#5B5FC7',
    primaryTextColor: '#ffffff',
    primaryBorderColor: '#4F52B2',
    lineColor: '#A0A3B1',
    secondaryColor: '#F0F2F9',
    tertiaryColor: '#E8F5E9',
    fontSize: '14px',
    fontFamily: '"Microsoft YaHei", "PingFang SC", sans-serif',
    nodeBorder: '#4F52B2',
    nodeTextColor: '#2D2D2D',
    titleColor: '#ffffff',
    edgeLabelBackground: '#ffffff',
    mainBkg: '#5B5FC7',
    nodeSecondaryBkg: '#F0F2F9',
    nodeTertiaryBkg: '#E8F5E9',
    clusterBkg: '#F8F9FC',
    clusterBorder: '#E2E4EB',
    labelTextColor: '#2D2D2D',
    labelBoxBkgColor: '#ffffff',
    labelBoxBorderColor: '#E2E4EB',
  },
  flowchart: {
    useMaxWidth: false,
    htmlLabels: true,
    curve: 'basis',
    padding: 25,
    nodeSpacing: 55,
    rankSpacing: 65,
  },
  securityLevel: 'loose',
})

const containerRef = ref(null)
const scale = ref(1)
const translateX = ref(0)
const translateY = ref(0)
const isDragging = ref(false)
const dragStartX = ref(0)
const dragStartY = ref(0)
const dragTranslateX = ref(0)
const dragTranslateY = ref(0)
const svgContent = ref('')
const loading = ref(true)
const error = ref('')

const MIN_SCALE = 0.2
const MAX_SCALE = 5.0
const ZOOM_STEP = 0.1

const diagramDefinition = `
flowchart TD
  classDef decision fill:#FFF4E6,stroke:#F59E0B,stroke-width:2px,color:#92400E,rx:8,ry:8
  classDef processA fill:#EEF2FF,stroke:#5B5FC7,stroke-width:1.5px,color:#3730A3,rx:6,ry:6
  classDef processB fill:#FFF3E0,stroke:#EA580C,stroke-width:1.5px,color:#7C2D12,rx:6,ry:6
  classDef processC fill:#F3E8FF,stroke:#9333EA,stroke-width:1.5px,color:#4C1D95,rx:6,ry:6
  classDef processD fill:#ECFDF5,stroke:#059669,stroke-width:1.5px,color:#064E3B,rx:6,ry:6
  classDef danger fill:#FEF2F2,stroke:#EF4444,stroke-width:2px,color:#991B1B,rx:6,ry:6
  classDef success fill:#DCFCE7,stroke:#16A34A,stroke-width:2px,color:#14532D,rx:6,ry:6
  classDef storage fill:#F8FAFC,stroke:#94A3B8,stroke-width:1.5px,color:#475569,rx:6,ry:6

  subgraph PURCHASE["📦 采购入库 · 主线A"]
    A1["🔬 质检员 · 到货登记<br/>IncomingReceipt<br/>PENDING_INSPECTION"]:::processA --> A2["🔬 质检员 · 来料检验<br/>IncomingInspection<br/>INSPECTED"]:::processA
    A2 --> A3{"检验结果"}:::decision
    A3 -->|"合格"| A4["📦 仓库管理员 · 合格入库<br/>WAREHOUSED → 原材料仓"]:::processA
    A3 -->|"不合格"| A5["📋 质检员 · 退货处理<br/>IncomingReturn · REJECTED"]:::danger
  end

  subgraph RMA["🔧 返厂维修 · 主线B"]
    D1["📋 售后专员 · 退货登记<br/>RmaReturn<br/>PENDING_DIAGNOSIS"]:::processB --> D2["🔬 测试工程师 · 故障诊断<br/>RmaDiagnosis<br/>DIAGNOSED"]:::processB
    D2 --> D3{"🔬 质量负责人 · 分配"}:::decision
    D3 -->|"外观问题"| D4["🔧 生产维修员 · 外观维修<br/>ASSIGNED"]:::processB
    D3 -->|"功能问题"| D5["🔬 测试工程师 · 功能维修<br/>ASSIGNED"]:::processB
    D3 -->|"判定报废"| D6["📋 质量负责人 · 报废申请<br/>PENDING_SCRAP"]:::danger
    D4 --> D7["🔧 维修工单<br/>RmaRepair · REPAIRING"]:::processB
    D5 --> D7
    D7 --> D8["已修复<br/>REPAIRED"]:::processB
    D8 --> D9{"🔬 质量负责人 · 质量检验<br/>RmaQualityCheck"}:::decision
    D9 -->|"PASS"| D10["检验通过<br/>QUALITY_CHECK"]:::processB
    D9 -->|"FAIL"| D4
    D10 --> D11["📦 仓库管理员 · 零成本仓入库<br/>RmaWarehouseIn · WAREHOUSED"]:::success
    D11 --> D12["📦 仓库管理员 · 再出货<br/>RmaReship · RESHIPPED"]:::processB
    D6 --> D13{"📦 仓库管理员 · 审批"}:::decision
    D13 -->|"同意"| D14["已报废<br/>SCRAPPED"]:::danger
    D13 -->|"驳回"| D3
  end

  subgraph SHIPMENT["🚚 出货流程 · 主线C"]
    C1["📦 仓库管理员 · 出货登记<br/>Shipment + SN<br/>→ OutboundOrder"]:::processC --> C2["📦 自动扣库存<br/>IN_STOCK → SOLD"]:::processC
  end

  subgraph PRODUCTION["🏭 生产制造 · 主线D"]
    B1["🔧 生产主管 · BOM管理<br/>BomHeader + BomDetail<br/>DRAFT → PUBLISHED"]:::processD --> B2["🔧 生产主管 · 生产任务<br/>ProductionTask · PENDING"]:::processD
    B2 --> B3["🔧 生产主管 · 生产中<br/>IN_PROGRESS · 领料 → 组装"]:::processD
    B3 --> B4["🔧 生产主管 · 生产完成<br/>COMPLETED"]:::processD
    B4 --> B5{"产出类型"}:::decision
    B5 -->|"成品"| B6["成品仓<br/>FINISHED"]:::storage
    B5 -->|"半成品"| B7["半成品仓<br/>SEMI_FINISHED"]:::storage
    B7 -.->|"继续生产"| B2
  end

  subgraph INVENTORY["🏗️ 库存体系 · InventoryItem"]
    E1["原材料仓<br/>RAW_MATERIAL"]:::storage
    E2["半成品仓<br/>SEMI_FINISHED"]:::storage
    E3["成品仓<br/>FINISHED"]:::storage
    E4["零成本仓-成品<br/>ZERO_COST_FINISHED"]:::success
    E5["零成本仓-半成品<br/>ZERO_COST_SEMI"]:::success
    E6["研发物料仓<br/>RND"]:::storage
  end

  A4 --> E1
  B6 --> E3
  B7 --> E2
  D11 --> E4
  D11 --> E5
  C2 --> E3

  style PURCHASE fill:#EEF2FF,stroke:#5B5FC7,stroke-width:2px,color:#3730A3
  style RMA fill:#FFF3E0,stroke:#EA580C,stroke-width:2px,color:#7C2D12
  style SHIPMENT fill:#F3E8FF,stroke:#9333EA,stroke-width:2px,color:#4C1D95
  style PRODUCTION fill:#ECFDF5,stroke:#059669,stroke-width:2px,color:#064E3B
  style INVENTORY fill:#F8FAFC,stroke:#94A3B8,stroke-width:2px,color:#475569
`

async function renderDiagram() {
  loading.value = true
  error.value = ''
  try {
    const { svg } = await mermaid.render('ims-workflow-diagram', diagramDefinition)
    svgContent.value = svg
    await nextTick()
    resetView()
    await nextTick()
    centerDiagram()
  } catch (e) {
    error.value = '流程图渲染失败：' + (e.message || e)
    console.error('Mermaid render error:', e)
  } finally {
    loading.value = false
  }
}

function resetView() {
  scale.value = 1
  translateX.value = 0
  translateY.value = 0
}

function centerDiagram() {
  if (!containerRef.value) return
  const svgEl = containerRef.value.querySelector('svg')
  if (!svgEl) return

  const container = containerRef.value
  const containerW = container.clientWidth
  const containerH = container.clientHeight
  const svgW = svgEl.getBBox ? svgEl.getBBox().width : svgEl.clientWidth || 1200
  const svgH = svgEl.getBBox ? svgEl.getBBox().height : svgEl.clientHeight || 800

  translateX.value = Math.max(0, (containerW - svgW) / 2)
  translateY.value = Math.max(0, (containerH - svgH) / 2)
}

function onWheel(e) {
  e.preventDefault()
  const delta = e.deltaY > 0 ? -ZOOM_STEP : ZOOM_STEP
  const newScale = Math.min(MAX_SCALE, Math.max(MIN_SCALE, scale.value + delta))
  if (newScale === scale.value) return

  const rect = containerRef.value.getBoundingClientRect()
  const mouseX = e.clientX - rect.left
  const mouseY = e.clientY - rect.top

  const scaleRatio = newScale / scale.value
  translateX.value = mouseX - (mouseX - translateX.value) * scaleRatio
  translateY.value = mouseY - (mouseY - translateY.value) * scaleRatio
  scale.value = newScale
}

function onMouseDown(e) {
  if (e.button !== 0) return
  isDragging.value = true
  dragStartX.value = e.clientX
  dragStartY.value = e.clientY
  dragTranslateX.value = translateX.value
  dragTranslateY.value = translateY.value
  e.preventDefault()
}

function onMouseMove(e) {
  if (!isDragging.value) return
  translateX.value = dragTranslateX.value + (e.clientX - dragStartX.value)
  translateY.value = dragTranslateY.value + (e.clientY - dragStartY.value)
}

function onMouseUp() {
  isDragging.value = false
}

function onMouseLeave() {
  isDragging.value = false
}

function zoomIn() {
  scale.value = Math.min(MAX_SCALE, scale.value + ZOOM_STEP * 2)
}

function zoomOut() {
  scale.value = Math.max(MIN_SCALE, scale.value - ZOOM_STEP * 2)
}

function fitToScreen() {
  if (!containerRef.value) return
  const svgEl = containerRef.value.querySelector('svg')
  if (!svgEl) return

  const container = containerRef.value
  const containerW = container.clientWidth - 40
  const containerH = container.clientHeight - 40
  const svgW = svgEl.getBBox ? svgEl.getBBox().width : svgEl.clientWidth || 1200
  const svgH = svgEl.getBBox ? svgEl.getBBox().height : svgEl.clientHeight || 800

  const scaleX = containerW / svgW
  const scaleY = containerH / svgH
  const newScale = Math.min(scaleX, scaleY, 1.0)
  scale.value = Math.max(MIN_SCALE, newScale)
  translateX.value = (containerW - svgW * scale.value) / 2
  translateY.value = (containerH - svgH * scale.value) / 2
}

onMounted(() => {
  renderDiagram()
})

onUnmounted(() => {
  document.removeEventListener('mousemove', onMouseMove)
  document.removeEventListener('mouseup', onMouseUp)
})
</script>

<template>
  <el-card class="workflow-page">
    <div class="toolbar">
      <h3 class="toolbar-title">IMS系统业务流程关系图</h3>
      <div class="toolbar-actions">
        <el-button-group>
          <el-button size="small" :icon="ZoomOut" @click="zoomOut" :disabled="scale <= MIN_SCALE">缩小</el-button>
          <el-button size="small" :icon="ZoomIn" @click="zoomIn" :disabled="scale >= MAX_SCALE">放大</el-button>
        </el-button-group>
        <el-button size="small" @click="fitToScreen">适应屏幕</el-button>
        <el-button size="small" @click="resetView">重置</el-button>
        <span class="scale-badge">{{ Math.round(scale * 100) }}%</span>
      </div>
    </div>

    <div
      ref="containerRef"
      class="diagram-container"
      :class="{ 'is-dragging': isDragging, 'is-loading': loading }"
      @wheel.prevent="onWheel"
      @mousedown="onMouseDown"
      @mousemove="onMouseMove"
      @mouseup="onMouseUp"
      @mouseleave="onMouseLeave"
    >
      <div v-if="loading" class="loading-state">
        <div class="loading-spinner" />
        <span>流程图加载中...</span>
      </div>
      <div v-else-if="error" class="error-state">
        <span class="error-icon">!</span>
        <span>{{ error }}</span>
      </div>
      <div
        v-else
        class="svg-wrapper"
        :style="{
          transform: `translate(${translateX}px, ${translateY}px) scale(${scale})`,
          transformOrigin: '0 0',
          cursor: isDragging ? 'grabbing' : 'grab',
        }"
        v-html="svgContent"
      />
    </div>

    <div class="legend">
      <span class="legend-item"><span class="legend-dot decision"></span> 判断节点</span>
      <span class="legend-item"><span class="legend-dot danger"></span> 报废/终止</span>
      <span class="legend-item"><span class="legend-dot success"></span> 零成本仓</span>
      <span class="legend-item"><span class="legend-dot primary"></span> 流程节点</span>
      <span class="legend-item"><span class="legend-dot subgraph"></span> 功能模块</span>
    </div>

    <div class="role-legend">
      <span class="role-title">数据表-状态流转：</span>
      <span class="role-item">A: IncomingReceipt → IncomingInspection → IncomingReturn</span>
      <span class="role-item">B: RmaReturn → RmaDiagnosis → RmaRepair → RmaQualityCheck → RmaWarehouseIn → RmaReship</span>
      <span class="role-item">C: Shipment → OutboundOrder → InventoryItem</span>
      <span class="role-item">D: BomHeader/BomDetail → ProductionTask</span>
    </div>
  </el-card>
</template>

<style scoped>
.workflow-page {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
}

.toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 24px;
  background: #fff;
  border-bottom: 1px solid #e8ecf1;
  flex-shrink: 0;
}

.toolbar-title {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  color: #1a1a2e;
}

.toolbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.scale-badge {
  display: inline-block;
  min-width: 50px;
  text-align: center;
  font-size: 13px;
  color: #64748b;
  font-variant-numeric: tabular-nums;
}

.diagram-container {
  flex: 1;
  position: relative;
  overflow: hidden;
  background: #fff;
  margin: 0;
  border-radius: 0;
  border: none;
}

.diagram-container.is-dragging {
  user-select: none;
}

.svg-wrapper {
  position: absolute;
  top: 0;
  left: 0;
  will-change: transform;
}

.svg-wrapper :deep(svg) {
  display: block;
}

.svg-wrapper :deep(.nodeLabel) {
  font-size: 13px !important;
  line-height: 1.5 !important;
}

.svg-wrapper :deep(.nodeLabel p) {
  margin: 0;
}

.svg-wrapper :deep(.edgeLabel) {
  font-size: 12px !important;
}

.svg-wrapper :deep(.edgeLabel span) {
  font-size: 12px !important;
}

.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  gap: 12px;
  color: #94a3b8;
  font-size: 14px;
}

.loading-spinner {
  width: 32px;
  height: 32px;
  border: 3px solid #e2e8f0;
  border-top-color: #4a6cf7;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-state {
  color: #ef4444;
}

.error-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #fef2f2;
  color: #ef4444;
  font-weight: 700;
  font-size: 18px;
}

.legend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 24px;
  padding: 10px 24px;
  background: #fafbfc;
  border-top: 1px solid #e8ecf1;
  flex-shrink: 0;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: #475569;
}

.legend-dot {
  display: inline-block;
  width: 14px;
  height: 14px;
  border-radius: 3px;
  border: 2px solid;
}

.legend-dot.decision {
  background: #fff7ed;
  border-color: #f97316;
}

.legend-dot.danger {
  background: #fef2f2;
  border-color: #ef4444;
}

.legend-dot.success {
  background: #f0fdf4;
  border-color: #22c55e;
}

.legend-dot.primary {
  background: #e8f0fe;
  border-color: #4a6cf7;
}

.legend-dot.subgraph {
  background: #f8fafc;
  border-color: #94a3b8;
}

.role-legend {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  gap: 10px;
  padding: 8px 24px;
  background: #f1f5f9;
  border-top: 1px solid #e8ecf1;
  flex-shrink: 0;
  flex-wrap: wrap;
}

.role-title {
  font-size: 12px;
  font-weight: 600;
  color: #475569;
  white-space: nowrap;
  padding: 2px 0;
}

.role-item {
  font-size: 11px;
  color: #334155;
  padding: 2px 8px;
  background: #fff;
  border-radius: 4px;
  border: 1px solid #e2e8f0;
  font-family: 'Consolas', 'Courier New', monospace;
  white-space: nowrap;
}
</style>