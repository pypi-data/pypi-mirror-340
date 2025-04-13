<script>
import { gqlAbsenceReasons } from "./helper.graphql";

export default {
  name: "AbsenceReasonButtons",
  data() {
    return {
      absenceReasons: [],
    };
  },
  apollo: {
    absenceReasons: {
      query: gqlAbsenceReasons,
      skip() {
        return this.customAbsenceReasons.length > 0;
      },
    },
  },
  props: {
    allowEmpty: {
      type: Boolean,
      default: false,
    },
    emptyValue: {
      type: [String, Number],
      required: false,
      default: "present",
    },
    customAbsenceReasons: {
      type: Array,
      required: false,
      default: () => [],
    },
  },
  computed: {
    innerAbsenceReasons() {
      if (this.customAbsenceReasons.length > 0) {
        return this.customAbsenceReasons;
      } else {
        return this.absenceReasons;
      }
    },
  },
  methods: {
    emit(value) {
      this.$emit("input", value);
      this.$emit("click", value);
    },
  },
};
</script>

<template>
  <div class="d-flex flex-wrap" style="gap: 0.5em">
    <v-skeleton-loader
      class="full-width d-flex flex-wrap child-flex-grow-1"
      style="gap: 0.5em"
      v-if="$apollo.queries.absenceReasons.loading"
      type="button@4"
    />
    <template v-else>
      <v-btn
        v-if="allowEmpty"
        outlined
        color="success"
        class="flex-grow-1"
        @click="emit(emptyValue)"
      >
        {{ $t("kolego.absence_reason.present") }}
      </v-btn>
      <v-btn
        v-for="absenceReason in innerAbsenceReasons"
        :key="'absence-reason-' + absenceReason.id"
        :color="absenceReason.colour"
        outlined
        class="flex-grow-1"
        @click="emit(absenceReason.id)"
      >
        {{ absenceReason.name }}
      </v-btn>
    </template>
  </div>
</template>

<style>
.child-flex-grow-1 > * {
  flex-grow: 1;
}
</style>
