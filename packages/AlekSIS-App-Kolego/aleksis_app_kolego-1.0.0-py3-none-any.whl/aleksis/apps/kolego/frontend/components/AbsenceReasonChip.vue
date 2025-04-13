<script>
import CounterChip from "aleksis.core/components/generic/chips/CounterChip.vue";

export default {
  name: "AbsenceReasonChip",
  components: { CounterChip },
  props: {
    absenceReason: {
      type: Object,
      required: true,
    },
    short: {
      type: Boolean,
      required: false,
      default: false,
    },
    loading: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  extends: CounterChip,
  computed: {
    text() {
      return this.short
        ? this.absenceReason.shortName
        : this.absenceReason.name;
    },
  },
};
</script>

<template>
  <counter-chip
    :color="absenceReason.colour"
    :value="absenceReason.id"
    :count="count"
    :only-show-count="onlyShowCount"
    outlined
    v-bind="$attrs"
    v-on="$listeners"
  >
    <slot name="prepend" />
    {{ text }}
    <slot name="append" />
    <v-avatar right v-if="loading">
      <v-progress-circular indeterminate :size="16" :width="2" />
    </v-avatar>
  </counter-chip>
</template>
