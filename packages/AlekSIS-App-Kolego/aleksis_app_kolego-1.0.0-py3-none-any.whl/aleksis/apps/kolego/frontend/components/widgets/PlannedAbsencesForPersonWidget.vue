<template>
  <v-card>
    <v-card-title>
      {{ $t("kolego.widgets.planned_absences.title") }}
    </v-card-title>
    <c-r-u-d-iterator
      i18n-key="alsijil.coursebook.statistics"
      :gql-query="gqlQuery"
      :gql-additional-query-args="gqlQueryArgs"
      :enable-create="false"
      :enable-edit="false"
      :enable-search="false"
      :enable-delete="true"
      :items-per-page="-1"
      :elevated="false"
      :hide-default-footer="true"
      :gql-delete-mutation="deleteMutation"
      :get-name-of-item="
        (item) =>
          `${$d($parseISODate(item.datetimeStart), 'shortDateTime')}–${$d(
            $parseISODate(item.datetimeEnd),
            'shortDateTime',
          )}, ${item.reason.name}`
      "
      ref="iterator"
    >
      <template #loading>
        <v-skeleton-loader type="list-item@5" />
      </template>
      <template #no-data>
        <div class="d-flex flex-column align-center justify-center">
          <mascot type="ready_for_items" width="33%" min-width="250px" />
          <div class="mb-4">
            {{ $t("kolego.widgets.planned_absences.no_data") }}
          </div>
        </div>
      </template>

      <template #default="{ items }">
        <v-list class="pa-0 scrollable-list">
          <div v-for="(item, idx) in items" :key="item.id">
            <v-list-item>
              <v-list-item-content>
                <v-list-item-title>
                  <template
                    v-if="
                      $parseISODate(item.datetimeStart).hasSame(
                        $parseISODate(item.datetimeEnd),
                        'day',
                      )
                    "
                  >
                    <time :datetime="item.datetimeStart" class="text-no-wrap">
                      <!-- eslint-disable-next-line @intlify/vue-i18n/no-raw-text -->
                      {{ $d($parseISODate(item.datetimeStart), "short") }},
                    </time>

                    <time :datetime="item.datetimeStart" class="text-no-wrap">
                      {{ $d($parseISODate(item.datetimeStart), "shortTime") }}
                    </time>
                    <span>–</span>
                    <time :datetime="item.datetimeEnd" class="text-no-wrap">
                      {{ $d($parseISODate(item.datetimeEnd), "shortTime") }}
                    </time>
                  </template>
                  <template v-else>
                    <time :datetime="item.datetimeStart" class="text-no-wrap">
                      {{
                        $d($parseISODate(item.datetimeStart), "shortDateTime")
                      }}
                    </time>
                    <span>–</span>
                    <time :datetime="item.datetimeEnd" class="text-no-wrap">
                      {{ $d($parseISODate(item.datetimeEnd), "shortDateTime") }}
                    </time>
                  </template>

                  <absence-reason-chip
                    :absence-reason="item.reason"
                    class="float-right"
                    small
                  />
                </v-list-item-title>
                <v-list-item-subtitle>
                  {{ item.comment }}
                </v-list-item-subtitle>
              </v-list-item-content>
              <v-list-item-icon>
                <v-btn
                  icon
                  color="red"
                  v-if="item.canDelete"
                  @click="$refs.iterator.$refs.bar.handleDelete(item)"
                >
                  <v-icon>$deleteContent</v-icon>
                </v-btn>
              </v-list-item-icon>
            </v-list-item>
            <v-divider v-if="idx + 1 < items.length" />
          </div>
        </v-list>
      </template>
    </c-r-u-d-iterator>
  </v-card>
</template>

<script>
import personOverviewCardMixin from "aleksis.core/mixins/personOverviewCardMixin.js";
import {
  plannedAbsencesForPerson,
  deletePlannedAbsences,
} from "./absences.graphql";
import CRUDIterator from "aleksis.core/components/generic/CRUDIterator.vue";
import AbsenceReasonChip from "../AbsenceReasonChip.vue";
import Mascot from "aleksis.core/components/generic/mascot/Mascot.vue";

export default {
  name: "PlannedAbsencesForPersonWidget",
  mixins: [personOverviewCardMixin],
  components: { Mascot, CRUDIterator, AbsenceReasonChip },
  data() {
    return {
      gqlQuery: plannedAbsencesForPerson,
      deleteMutation: deletePlannedAbsences,
    };
  },
  computed: {
    gqlQueryArgs() {
      return {
        person: this.person.id,
      };
    },
  },
};
</script>
<style scoped>
.scrollable-list {
  max-height: 350px;
  overflow-y: scroll;
}
</style>
