<template>
  <LayoutHeader v-if="salesCampaign.doc">
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon v-if="item.icon" :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
    </template>
  </LayoutHeader>
  <div v-if="salesCampaign.doc" ref="parentRef" class="flex h-full">
    <Resizer
      v-if="salesCampaign.doc"
      :parent="$refs.parentRef"
      class="flex h-full flex-col overflow-hidden border-r"
    >
      <div class="border-b">
        
          <div>
            <div class="flex flex-col items-start justify-start gap-4 p-5">
             <div class="flex gap-4 items-center">
                <div class="flex flex-col gap-2 truncate">
                  <div class="truncate text-2xl font-medium text-ink-gray-9">
                    <span>{{ salesCampaign.doc.name }}</span>
                  </div>
                  <div
                    v-if="salesCampaign.doc.campaign_owner"
                    class="flex items-center gap-1.5 text-base text-ink-gray-8"
                  >
                    <Avatar
                    v-if="salesCampaign.doc.campaign_owner"
                    class="flex items-center"
                    :image="getUser(salesCampaign.doc.campaign_owner).user_image"
                    :label="getUser(salesCampaign.doc.campaign_owner).full_name"
                    size="xs"
                  />
                    <span>{{ salesCampaign.doc.campaign_owner }}</span>
                  </div>
                  <ErrorMessage :message="__(error)" />
                </div>
              </div>
              <div class="flex gap-1.5">
                <Button
                  :label="__('Delete')"
                  theme="red"
                  size="sm"
                  iconLeft="trash-2"
                  @click="deleteSalesCampaign()"
                />
                <Button
                  :tooltip="__('Edit LinkedIn Chat Sequence')"
                  icon="link"
                  @click="openLinkedInChatSequence"
                />
              </div>
            </div>
          </div>
      </div>
      <div
        v-if="sections.data"
        class="flex flex-1 flex-col justify-between overflow-hidden"
      >
        <SidePanelLayout
          :sections="sections.data"
          doctype="CRM Sales Campaign"
          :docname="salesCampaign.doc.name"
          @reload="sections.reload"
        />
      </div>
    </Resizer>
    <Tabs as="div" v-model="tabIndex" :tabs="tabs">
      <template #tab-item="{ tab, selected }">
        <button
          class="group flex items-center gap-2 border-b border-transparent py-2.5 text-base text-ink-gray-5 duration-300 ease-in-out hover:border-outline-gray-3 hover:text-ink-gray-9"
          :class="{ 'text-ink-gray-9': selected }"
        >
          <component v-if="tab.icon" :is="tab.icon" class="h-5" />
          {{ __(tab.label) }}
          <Badge
            class="group-hover:bg-surface-gray-7"
            :class="[selected ? 'bg-surface-gray-7' : 'bg-gray-600']"
            variant="solid"
            theme="gray"
            size="sm"
          >
            {{ tab.count }}
          </Badge>
        </button>
      </template>
      <template #tab-panel="{ tab }">
        <OrganizationsListView
          class="mt-4"
          v-if="tab.label === 'Organizations' && rows.length"
          :rows="rows"
          :columns="columns"
          :options="{ resizeColumn: false, showTooltip: false }"
        />
        <LeadsListView
          class="mt-4"
          v-if="tab.label === 'Leads' && rows.length"
          :rows="rows"
          :columns="columns"
          :options="{ selectable: false, showTooltip: false }"
        />
        <div
          v-if="!rows.length"
          class="grid flex-1 place-items-center text-xl font-medium text-ink-gray-4"
        >
          <div class="flex flex-col items-center justify-center space-y-3">
            <component :is="tab.icon" class="!h-10 !w-10" />
            <div>{{ __('No {0} Found', [__(tab.label)]) }}</div>
          </div>
        </div>
      </template>
    </Tabs>
  </div>
  <ErrorPage
    v-else-if="errorTitle"
    :errorTitle="errorTitle"
    :errorMessage="errorMessage"
  />
  <DeleteLinkedDocModal
    v-if="showDeleteLinkedDocModal"
    v-model="showDeleteLinkedDocModal"
    :doctype="'CRM Sales Campaign'"
    :docname="props.salesCampaignId"
    name="SalesCampaigns"
  />
</template>

<script setup>
import ErrorPage from '@/components/ErrorPage.vue'
import Resizer from '@/components/Resizer.vue'
import SidePanelLayout from '@/components/SidePanelLayout.vue'
import Icon from '@/components/Icon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import LeadsListView from '@/components/ListViews/LeadsListView.vue'
import OrganizationsListView from '@/components/ListViews/OrganizationsListView.vue'
import LeadsIcon from '@/components/Icons/LeadsIcon.vue'
import OrganizationsIcon from '@/components/Icons/OrganizationsIcon.vue'
import { useDocument } from '@/data/document'
import { getSettings } from '@/stores/settings'
import { getMeta } from '@/stores/meta'
import { usersStore } from '@/stores/users'
import { statusesStore } from '@/stores/statuses'
import { getView } from '@/utils/view'
import { formatDate, timeAgo, website } from '@/utils'
import {
  Breadcrumbs,
  Avatar,
  Tabs,
  createListResource,
  usePageMeta,
  createResource,
} from 'frappe-ui'
import { h, computed, ref, toDisplayString } from 'vue'
import { useRoute } from 'vue-router'
import DeleteLinkedDocModal from '@/components/DeleteLinkedDocModal.vue'

const props = defineProps({
  salesCampaignId: {
    type: String,
    required: true,
  },
})

const { brand } = getSettings()
const { getUser } = usersStore()
const { getLeadStatus } = statusesStore()
const { doctypeMeta } = getMeta('CRM Sales Campaign')
const { getFormattedCurrency } =
  getMeta('CRM Organization')

const route = useRoute()

const errorTitle = ref('')
const errorMessage = ref('')

const showDeleteLinkedDocModal = ref(false)

const { document: salesCampaign } = useDocument(
  'CRM Sales Campaign',
  props.salesCampaignId,
)

const breadcrumbs = computed(() => {
  let items = [{ label: __('SalesCampaigns'), route: { name: 'SalesCampaigns' } }]

  if (route.query.view || route.query.viewType) {
    let view = getView(
      route.query.view,
      route.query.viewType,
      'CRM Sales Campaign',
    )
    if (view) {
      items.push({
        label: __(view.label),
        icon: view.icon,
        route: {
          name: 'SalesCampaigns',
          params: { viewType: route.query.viewType },
          query: { view: route.query.view },
        },
      })
    }
  }

  items.push({
    label: title.value,
    route: {
      name: 'SalesCampaign',
      params: { salesCampaignId: props.salesCampaignId },
    },
  })
  return items
})

const title = computed(() => {
  let t = doctypeMeta['CRM Sales Campaign']?.title_field || 'name'
  return salesCampaign.doc?.[t] || props.salesCampaignId
})

usePageMeta(() => {
  return {
    title: title.value,
    icon: brand.favicon,
  }
})

async function deleteSalesCampaign() {
  showDeleteLinkedDocModal.value = true
}

function openLinkedInChatSequence() {
  window.open(`/app/crm-sales-campaign/${salesCampaign.doc.name}`, '_blank')
}

const sections = createResource({
  url: 'crm.fcrm.doctype.crm_fields_layout.crm_fields_layout.get_sidepanel_sections',
  cache: ['sidePanelSections', 'CRM Sales Campaign'],
  params: { doctype: 'CRM Sales Campaign' },
  auto: true,
  transform: (data) => data,
})



const tabIndex = ref(0)
const tabs = [
  {
    label: 'Organizations',
    icon: h(OrganizationsIcon, { class: 'h-4 w-4' }),
    count: computed(() => organizations.data?.length),
  },
  {
    label: 'Leads',
    icon: h(LeadsIcon, { class: 'h-4 w-4' }),
    count: computed(() => leads.data?.length),
  },
]

const leads = createListResource({
  type: 'list',
  doctype: 'CRM Lead',
  cache: ['leads', props.salesCampaignId],
  fields: [
    "name",
    "lead_name",
    "organization",
    "status",
    "sales_campaign",
    "email",
    "lead_owner",
    "first_name",
    "modified",
    "_assign",
    "image",
  ],
  filters: {
    sales_campaign: props.salesCampaignId,
  },
  orderBy: 'modified desc',
  pageLength: 20,
  auto: true,
})

const organizations = createListResource({
  type: 'list',
  doctype: 'CRM Organization',
  cache: ['organizations', props.salesCampaignId],
  fields: [
    'name',
    'organization_name',
    'organization_logo',
    'website',
    'territory',
    'industry',
    'sales_campaign',
    'modified',
  ],
  filters: {
    sales_campaign: props.salesCampaignId,
  },
  orderBy: 'modified desc',
  pageLength: 20,
  auto: true,
})

const rows = computed(() => {
  let list = []
  list = !tabIndex.value ? organizations : leads

  if (!list.data) return []
  return list.data.map((row) => {
    return !tabIndex.value ?  getOrganizationRowObject(row) : getLeadRowObject(row)
  })
})

const columns = computed(() => {
  return tabIndex.value === 0 ?  organizationColumns : leadColumns 
})

function getLeadRowObject(lead) {
  return {
    lead_name: {
        label: lead.lead_name,
        image: lead.image,
        image_label: lead.first_name,
    },
    name: lead.name,
    salesCampaign: lead.sales_campaign,
    linkedin_url: lead.linkedin_url,
    organization: lead.organization,
    status: {
      label: lead.status,
      color: getLeadStatus(lead.status)?.color,
    },
    email: lead.email,
    mobile_no: lead.mobile_no,
    lead_owner: {
      label: lead.lead_owner && getUser(lead.lead_owner).full_name,
      ...(lead.lead_owner && getUser(lead.lead_owner)),
    },
    modified: {
      label: formatDate(lead.modified),
      timeAgo: __(timeAgo(lead.modified)),
    },
  }
}

function getOrganizationRowObject(organization) {
  return {
    name: organization.name,
    organization_name: {
          label: organization.organization_name,
          logo: organization.organization_logo,
        },
    website: website(organization.website),
    territory: organization.territory,
    industry: organization.industry,
    annual_revenue: getFormattedCurrency('annual_revenue', organization),
    modified: {
      label: formatDate(organization.modified),
      timeAgo: __(timeAgo(organization.modified)),
    },
  }
}

const leadColumns = [
  {
    label: __('Name'),
    key: 'lead_name',
    align: 'left',
    width: '12rem',
  },
  {
    label: __('Organization'),
    key: 'organization',
    width: '12rem',
  },
  {
    label: __('Status'),
    key: 'status',
    width: '10rem',
  },
  {
    label: __('Lead owner'),
    key: 'lead_owner',
    width: '10rem',
  },
  {
    label: __('Last modified'),
    key: 'modified',
    width: '8rem',
  },
]

const organizationColumns = [
  {
    label: __('Organization'),
    key: 'organization_name',
    width: '12rem',
  },
  {
    label: __('Website'),
    key: 'website',
    width: '10rem',
  },
  {
    label: __('Territory'),
    key: 'territory',
    width: '8rem',
  },
  {
    label: __('Annual Revenue'),
    key: 'annual_revenue',
    width: '10rem',
  },
  {
    label: __('Last modified'),
    key: 'modified',
    width: '8rem',
  },
]

</script>
