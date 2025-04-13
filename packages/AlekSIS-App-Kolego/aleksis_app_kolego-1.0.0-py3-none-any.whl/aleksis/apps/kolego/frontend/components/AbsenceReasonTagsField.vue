<script setup>
import ForeignKeyField from "aleksis.core/components/generic/forms/ForeignKeyField.vue";
</script>

<template>
  <foreign-key-field
    v-bind="$attrs"
    v-on="$listeners"
    :fields="headers"
    create-item-i18n-key="kolego.absence_reason_tag.create"
    :gql-query="gqlQuery"
    :gql-create-mutation="gqlCreateMutation"
    :gql-patch-mutation="{}"
    :default-item="defaultItem"
    multiple
    chips
  >
    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #name.field="{ attrs, on }">
      <div aria-required="true">
        <v-text-field
          v-bind="attrs"
          v-on="on"
          :rules="$rules().required.build()"
        />
      </div>
    </template>

    <!-- eslint-disable-next-line vue/valid-v-slot -->
    <template #shortName.field="{ attrs, on }">
      <div aria-required="true">
        <v-text-field
          v-bind="attrs"
          v-on="on"
          :rules="$rules().required.build()"
        />
      </div>
    </template>
  </foreign-key-field>
</template>

<script>
import {
  allAbsenceReasonTags,
  createAbsenceReasonTags,
} from "./absenceReasonTags.graphql";
import formRulesMixin from "aleksis.core/mixins/formRulesMixin.js";

export default {
  name: "AbsenceReasonTagsField",
  mixins: [formRulesMixin],
  data() {
    return {
      headers: [
        {
          text: this.$t("kolego.absence_reason_tag.short_name"),
          value: "shortName",
        },
        {
          text: this.$t("kolego.absence_reason_tag.name"),
          value: "name",
        },
      ],
      i18nKey: "kolego.absence_reason_tag",
      gqlQuery: allAbsenceReasonTags,
      gqlCreateMutation: createAbsenceReasonTags,
      defaultItem: {
        name: "",
        shortName: "",
      },
    };
  },
};
</script>

<style scoped></style>
