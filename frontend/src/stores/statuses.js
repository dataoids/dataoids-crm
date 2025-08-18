import IndicatorIcon from '@/components/Icons/IndicatorIcon.vue'
import { capture } from '@/telemetry'
import { parseColor } from '@/utils'
import { defineStore } from 'pinia'
import { createListResource } from 'frappe-ui'
import { reactive, h } from 'vue'

export const statusesStore = defineStore('crm-statuses', () => {
  let leadStatusesByName = reactive({})
  let leadLinkedinStatusesByName = reactive({})
  let leadEmailStatusesByName = reactive({})
  let dealStatusesByName = reactive({})
  let communicationStatusesByName = reactive({})

  const leadStatuses = createListResource({
    doctype: 'CRM Lead Status',
    fields: ['name', 'color', 'position'],
    orderBy: 'position asc',
    cache: 'lead-statuses',
    initialData: [],
    auto: true,
    transform(statuses) {
      for (let status of statuses) {
        status.color = parseColor(status.color)
        leadStatusesByName[status.name] = status
      }
      return statuses
    },
  })

  const leadLinkedinStatuses = createListResource({
    doctype: 'CRM Lead LinkedIn Status',
    fields: ['name', 'color', 'position'],
    orderBy: 'position asc',
    cache: 'lead-linkedin-statuses',
    initialData: [],
    auto: true,
    transform(statuses) {
      for (let status of statuses) {
        status.color = parseColor(status.color)
        leadLinkedinStatusesByName[status.name] = status
      }
      return statuses
    },
  })

  const leadEmailStatuses = createListResource({
    doctype: 'CRM Lead Email Status',
    fields: ['name', 'color', 'position'],
    orderBy: 'position asc',
    cache: 'lead-email-statuses',
    initialData: [],
    auto: true,
    transform(statuses) {
      for (let status of statuses) {
        status.color = parseColor(status.color)
        leadEmailStatusesByName[status.name] = status
      }
      return statuses
    },
  })

  const dealStatuses = createListResource({
    doctype: 'CRM Deal Status',
    fields: ['name', 'color', 'position', 'type'],
    orderBy: 'position asc',
    cache: 'deal-statuses',
    initialData: [],
    auto: true,
    transform(statuses) {
      for (let status of statuses) {
        status.color = parseColor(status.color)
        dealStatusesByName[status.name] = status
      }
      return statuses
    },
  })

  const communicationStatuses = createListResource({
    doctype: 'CRM Communication Status',
    fields: ['name'],
    cache: 'communication-statuses',
    initialData: [],
    auto: true,
    transform(statuses) {
      for (let status of statuses) {
        communicationStatusesByName[status.name] = status
      }
      return statuses
    },
  })

  function getLeadStatus(name) {
    if (!name) {
      name = leadStatuses.data[0].name
    }
    return leadStatusesByName[name]
  }

  function getLeadLinkedinStatus(name) {
    if (!name) {
      name = leadLinkedinStatuses.data[0].name
    }
    return leadLinkedinStatusesByName[name]
  }

  function getLeadEmailStatus(name) {
    if (!name) {
      name = leadEmailStatuses.data[0].name
    }
    return leadEmailStatusesByName[name]
  }

  function getDealStatus(name) {
    if (!name) {
      name = dealStatuses.data[0].name
    }
    return dealStatusesByName[name]
  }

  function getCommunicationStatus(name) {
    if (!name) {
      name = communicationStatuses.data[0].name
    }
    return communicationStatuses[name]
  }

  function statusOptions(doctype, statuses = [], triggerStatusChange = null) {
    let statusesByName
    if (doctype === 'deal') {
      statusesByName = dealStatusesByName
    } else if (doctype === 'lead-linkedin') {
      statusesByName = leadLinkedinStatusesByName
    } else if (doctype === 'lead-email') {
      statusesByName = leadEmailStatusesByName
    } else if (doctype === 'lead') {
      statusesByName = leadStatusesByName
    } else {
      statusesByName = leadStatusesByName
    }

    if (statuses?.length) {
      statusesByName = statuses.reduce((acc, status) => {
        acc[status] = statusesByName[status]
        return acc
      }, {})
    }

    let options = []
    for (const status in statusesByName) {
      options.push({
        label: statusesByName[status]?.name,
        value: statusesByName[status]?.name,
        icon: () => h(IndicatorIcon, { class: statusesByName[status]?.color }),
        onClick: async () => {
          await triggerStatusChange?.(statusesByName[status]?.name)
          capture('status_changed', { doctype, status })
        },
      })
    }
    return options
  }

  return {
    leadStatuses,
    leadLinkedinStatuses,
    leadEmailStatuses,
    dealStatuses,
    communicationStatuses,
    getLeadStatus,
    getLeadLinkedinStatus,
    getLeadEmailStatus,
    getDealStatus,
    getCommunicationStatus,
    statusOptions,
  }
})
