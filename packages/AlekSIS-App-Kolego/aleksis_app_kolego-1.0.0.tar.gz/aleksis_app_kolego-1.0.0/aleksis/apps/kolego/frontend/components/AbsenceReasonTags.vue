<script setup>
import InlineCRUDList from "aleksis.core/components/generic/InlineCRUDList.vue";
</script>

<template>
  <v-container>
    <inline-c-r-u-d-list
      :headers="headers"
      :i18n-key="i18nKey"
      create-item-i18n-key="kolego.absence_reason_tag.create"
      :gql-query="gqlQuery"
      :gql-create-mutation="gqlCreateMutation"
      :gql-patch-mutation="gqlPatchMutation"
      :gql-delete-mutation="gqlDeleteMutation"
      :default-item="defaultItem"
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
    </inline-c-r-u-d-list>
  </v-container>
</template>

<script>
import formRulesMixin from "aleksis.core/mixins/formRulesMixin.js";
import {
  absenceReasonTags,
  createAbsenceReasonTags,
  deleteAbsenceReasonTags,
  updateAbsenceReasonTags,
} from "./absenceReasonTags.graphql";

export default {
  name: "AbsenceReasonTags",
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
      gqlQuery: absenceReasonTags,
      gqlCreateMutation: createAbsenceReasonTags,
      gqlPatchMutation: updateAbsenceReasonTags,
      gqlDeleteMutation: deleteAbsenceReasonTags,
      defaultItem: {
        shortName: "",
        name: "",
      },
    };
  },
};
</script>

<style scoped></style>
