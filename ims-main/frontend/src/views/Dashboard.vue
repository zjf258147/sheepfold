<script setup>
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { OfficeBuilding, Monitor, Location, Warning, Tickets, Box } from '@element-plus/icons-vue'
import { getPartnerSummary, getPendingAudit, getPhase2Stats, getStockSummary } from '@/api/dashboard'
import {
  partnerTotalOutbound,
  inStockDetailTooltipLines,
  qtyCellClass,
  skuRowTotal,
  skuSummaryMethod,
} from '@/utils/inventorySummary'

const router = useRouter()
const pending = ref({ inbound_pending: 0, outbound_pending: 0 })
const phase2 = ref({ station_total: 0, station_active: 0, device_total: 0, device_running: 0, device_fault: 0, device_recycled: 0, stocktake_in_progress: 0, stocktake_completed: 0, pending_adjustments: 0, warranty_expiring_soon: 0 })
const summary = ref([])
const partnerSummary = ref([])
const loading = ref(false)

onMounted(loadData)

async function loadData() {
  loading.value = true
  try {
    const [p, s, ps, p2] = await Promise.all([getPendingAudit(), getStockSummary(), getPartnerSummary(), getPhase2Stats()])
    pending.value = p.data
    phase2.value = p2.data
    summary.value = s.data.items
    partnerSummary.value = [...ps.data.items].sort(
      (a, b) => partnerTotalOutbound(b) - partnerTotalOutbound(a),
    )
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div v-loading="loading">
    <el-row :gutter="20" class="cards">
      <el-col :span="12">
        <el-card shadow="hover" class="audit-card outbound" @click="router.push('/outbound')">
          <div class="card-num">{{ pending.outbound_pending }}</div>
          <div class="card-label">待审核出库单</div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover" class="audit-card inbound" @click="router.push('/inbound')">
          <div class="card-num">{{ pending.inbound_pending }}</div>
          <div class="card-label">待审核入库单</div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" class="cards" style="margin-top:16px">
      <el-col :span="4">
        <el-card shadow="hover" class="phase2-card station" @click="router.push('/station')">
          <div class="p2-icon"><el-icon :size="28"><Location /></el-icon></div>
          <div class="p2-num">{{ phase2.station_active }}<small>/{{ phase2.station_total }}</small></div>
          <div class="p2-label">活跃场站</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="phase2-card device" @click="router.push('/device-ledger')">
          <div class="p2-icon"><el-icon :size="28"><Monitor /></el-icon></div>
          <div class="p2-num">{{ phase2.device_running }}<small>/{{ phase2.device_total }}</small></div>
          <div class="p2-label">运行中设备</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="phase2-card fault">
          <div class="p2-icon"><el-icon :size="28"><Warning /></el-icon></div>
          <div class="p2-num">{{ phase2.device_fault }}</div>
          <div class="p2-label">故障设备</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="phase2-card stocktake" @click="router.push('/stocktake')">
          <div class="p2-icon"><el-icon :size="28"><Tickets /></el-icon></div>
          <div class="p2-num">{{ phase2.stocktake_in_progress }}<small>/{{ phase2.stocktake_in_progress + phase2.stocktake_completed }}</small></div>
          <div class="p2-label">进行中盘点</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="phase2-card adjustment" @click="router.push('/adjustment')">
          <div class="p2-icon"><el-icon :size="28"><Box /></el-icon></div>
          <div class="p2-num">{{ phase2.pending_adjustments }}</div>
          <div class="p2-label">库存调整</div>
        </el-card>
      </el-col>
      <el-col :span="4">
        <el-card shadow="hover" class="phase2-card warranty" @click="router.push('/device-ledger')">
          <div class="p2-icon"><el-icon :size="28"><Warning /></el-icon></div>
          <div class="p2-num">{{ phase2.warranty_expiring_soon }}</div>
          <div class="p2-label">质保将到期</div>
        </el-card>
      </el-col>
    </el-row>

    <el-card shadow="never" style="margin-top:20px">
      <template #header><span>实时库存统计（按 SKU）</span></template>
      <el-table
        :data="summary"
        stripe
        border
        show-summary
        :summary-method="skuSummaryMethod"
        :cell-class-name="qtyCellClass"
      >
        <el-table-column prop="sku_name" label="商品名称" min-width="150" />
        <el-table-column prop="in_stock" label="在库" align="center">
          <template #default="{ row }">
            <el-tooltip v-if="inStockDetailTooltipLines(row).length" placement="top">
              <template #content>
                <div v-for="line in inStockDetailTooltipLines(row)" :key="line.label" class="in-stock-tooltip-line">
                  {{ line.label }}：{{ line.qty }}
                </div>
              </template>
              <span class="in-stock-cell">{{ row.in_stock }}</span>
            </el-tooltip>
            <span v-else>{{ row.in_stock }}</span>
          </template>
        </el-table-column>
        <el-table-column label="不在库" align="center">
          <el-table-column prop="sold" label="售出-线上" align="center" />
          <el-table-column prop="sold_offline" label="售出-线下" align="center" />
          <el-table-column prop="presold" label="准售出" align="center" />
          <el-table-column prop="borrowed" label="借出" align="center" />
          <el-table-column prop="gifted" label="赠送" align="center" />
          <el-table-column prop="scrapped" label="损毁" align="center" />
          <el-table-column prop="rnd" label="研发" align="center" />
          <el-table-column prop="sample" label="样机" align="center" />
          <el-table-column prop="trial" label="试用" align="center" />
          <el-table-column prop="repair" label="维修" align="center" />
          <el-table-column prop="dept_procurement" label="部门采购" align="center" />
        </el-table-column>
        <el-table-column label="统计" min-width="90" align="center">
          <template #default="{ row }">{{ skuRowTotal(row) }}</template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-card shadow="never" style="margin-top:20px">
      <template #header><span>出库商品统计（按关联单位）</span></template>
      <el-table :data="partnerSummary" stripe border :cell-class-name="qtyCellClass">
        <el-table-column label="关联单位" min-width="140" show-overflow-tooltip>
          <template #default="{ row }">
            <span class="partner-name-cell">
              {{ row.partner_name || '—' }}
              <el-tooltip v-if="row.partner_group_name" :content="row.partner_group_name" placement="top">
                <el-icon class="partner-group-icon"><OfficeBuilding /></el-icon>
              </el-tooltip>
            </span>
          </template>
        </el-table-column>
        <el-table-column label="累计" min-width="90" align="center">
          <template #default="{ row }">{{ partnerTotalOutbound(row) }}</template>
        </el-table-column>
        <el-table-column label="售出-出库" align="center">
          <el-table-column prop="sold" label="售出-线上" align="center" />
          <el-table-column prop="sold_offline" label="售出-线下" align="center" />
          <el-table-column prop="presold" label="准售出" align="center" />
        </el-table-column>
        <el-table-column label="其他-出库" align="center">
          <el-table-column prop="borrowed" label="借出" align="center" />
          <el-table-column prop="gifted" label="赠送" align="center" />
          <el-table-column prop="scrapped" label="损毁" align="center" />
          <el-table-column prop="rnd" label="研发" align="center" />
          <el-table-column prop="sample" label="样机" align="center" />
          <el-table-column prop="trial" label="试用" align="center" />
          <el-table-column prop="repair" label="维修" align="center" />
          <el-table-column prop="dept_procurement" label="部门采购" align="center" />
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<style scoped>
.audit-card { cursor: pointer; text-align: center; padding: 20px 0; }
.card-num { font-size: 48px; font-weight: 700; }
.card-label { font-size: 16px; color: #606266; margin-top: 8px; }
.outbound .card-num { color: #e6a23c; }
.inbound .card-num { color: #7b67ee; }
.partner-name-cell { display: inline-flex; align-items: center; gap: 4px; }
.partner-group-icon { font-size: 14px; color: #909399; cursor: help; flex-shrink: 0; }
.partner-group-icon:hover { color: #409eff; }
:deep(.qty-zero) { color: #c0c4cc; }
.in-stock-cell { cursor: help; border-bottom: 1px dashed #c0c4cc; }
:deep(.el-table__footer-wrapper td.el-table__cell .cell) {
  color: #303133;
  font-weight: 600;
}

.phase2-card { cursor: pointer; text-align: center; padding: 12px 4px; }
.phase2-card:hover { transform: translateY(-2px); }
.p2-icon { margin-bottom: 6px; }
.p2-num { font-size: 22px; font-weight: 700; }
.p2-num small { font-size: 13px; font-weight: 400; color: #909399; }
.p2-label { font-size: 12px; color: #909399; margin-top: 2px; }
.station .p2-icon { color: #409eff; }
.station .p2-num { color: #409eff; }
.device .p2-icon { color: #67c23a; }
.device .p2-num { color: #67c23a; }
.fault .p2-icon { color: #f56c6c; }
.fault .p2-num { color: #f56c6c; }
.stocktake .p2-icon { color: #e6a23c; }
.stocktake .p2-num { color: #e6a23c; }
.adjustment .p2-icon { color: #7b67ee; }
.adjustment .p2-num { color: #7b67ee; }
.warranty .p2-icon { color: #f56c6c; }
.warranty .p2-num { color: #f56c6c; }
</style>