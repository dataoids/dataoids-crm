<template>
  <LayoutHeader>
    <template #left-header>
      <ViewBreadcrumbs v-model="viewControls" routeName="SalesCampaigns" />
    </template>
    <template #right-header>
      <CustomActions
        v-if="salesCampaignsListView?.customListActions"
        :actions="salesCampaignsListView.customListActions"
      />
      <Button
        variant="solid"
        :label="__('Create')"
        @click="showSalesCampaignModal = true"
      >
        <template #prefix><FeatherIcon name="plus" class="h-4" /></template>
      </Button>
    </template>
  </LayoutHeader>
  <ViewControls
    ref="viewControls"
    v-model="salesCampaigns"
    v-model:loadMore="loadMore"
    v-model:resizeColumn="triggerResize"
    v-model:updatedPageCount="updatedPageCount"
    doctype="CRM Sales Campaign"
  />
  <SalesCampaignsListView
    ref="salesCampaignsListView"
    v-if="salesCampaigns.data && rows.length"
    v-model="salesCampaigns.data.page_length_count"
    v-model:list="salesCampaigns"
    :rows="rows"
    :columns="salesCampaigns.data.columns"
    :options="{
      showTooltip: false,
      resizeColumn: true,
      rowCount: salesCampaigns.data.row_count,
      totalCount: salesCampaigns.data.total_count,
    }"
    @loadMore="() => loadMore++"
    @columnWidthUpdated="() => triggerResize++"
    @updatePageCount="(count) => (updatedPageCount = count)"
    @applyFilter="(data) => viewControls.applyFilter(data)"
    @applyLikeFilter="(data) => viewControls.applyLikeFilter(data)"
    @likeDoc="(data) => viewControls.likeDoc(data)"
    @selectionsChanged="
      (selections) => viewControls.updateSelections(selections)
    "
  />
  <div
    v-else-if="salesCampaigns.data"
    class="flex h-full items-center justify-center"
  >
    <div
      class="flex flex-col items-center gap-3 text-xl font-medium text-ink-gray-4"
    >
      <MoneyIcon class="h-10 w-10" />
      <span>{{ __('No {0} Found', [__('Sales Campaigns')]) }}</span>
      <Button :label="__('Create')" @click="showSalesCampaignModal = true">
        <template #prefix><FeatherIcon name="plus" class="h-4" /></template>
      </Button>
    </div>
  </div>
  <SalesCampaignModal
    v-if="showSalesCampaignModal"
   v-model="showSalesCampaignModal"
  />
</template>
<script setup>
import ViewBreadcrumbs from '@/components/ViewBreadcrumbs.vue'
import CustomActions from '@/components/CustomActions.vue'
import MoneyIcon from '@/components/Icons/MoneyIcon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import SalesCampaignModal from '@/components/Modals/SalesCampaignModal.vue'
import SalesCampaignsListView from '@/components/ListViews/SalesCampaignsListView.vue'
import ViewControls from '@/components/ViewControls.vue'
import { usersStore } from '@/stores/users'
import { formatDate, timeAgo } from '@/utils'
import { ref, computed } from 'vue'


const showSalesCampaignModal = ref(false)
// salesCampaigns data is loaded in the ViewControls component
const salesCampaigns = ref({})
const loadMore = ref(1)
const triggerResize = ref(1)
const updatedPageCount = ref(20)
const { getUser } = usersStore()
const viewControls = ref(null)

const rows = computed(() => {
  if (
    !salesCampaigns.value?.data?.data ||
    !['list', 'group_by'].includes(salesCampaigns.value.data.view_type)
  )
    return []
  return salesCampaigns.value?.data.data.map((salesCampaign) => {
    let _rows = {}
    salesCampaigns.value?.data.rows.forEach((row) => {
      _rows[row] = salesCampaign[row]

      let fieldType = salesCampaigns.value?.data.columns?.find(
        (col) => (col.key || col.value) == row,
      )?.type

      if (
        fieldType &&
        ['Date', 'Datetime'].includes(fieldType) &&
        !['modified', 'creation'].includes(row)
      ) {
        _rows[row] = formatDate(
          salesCampaign[row],
          '',
          true,
          fieldType == 'Datetime',
        )
      }

      if (['modified', 'creation'].includes(row)) {
        _rows[row] = {
          label: formatDate(salesCampaign[row]),
          timeAgo: __(timeAgo(salesCampaign[row])),
        }
      } else if (row == 'campaign_owner') {
        _rows[row] = {
          label: salesCampaign.campaign_owner && getUser(salesCampaign.campaign_owner).full_name,
          ...(salesCampaign.campaign_owner && getUser(salesCampaign.campaign_owner)),
        }
      }
    })
    return _rows
  })
})
</script>
