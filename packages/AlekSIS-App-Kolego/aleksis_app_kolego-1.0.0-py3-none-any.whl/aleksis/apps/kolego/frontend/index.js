export const collectionItems = {
  corePersonWidgets: [
    {
      key: "core-person-widgets",
      component: () =>
        import("./components/widgets/PlannedAbsencesForPersonWidget.vue"),
      shouldDisplay: () => true,
      colProps: {
        cols: 12,
        md: 6,
        lg: 4,
      },
    },
  ],
};

export default {
  meta: {
    inMenu: true,
    titleKey: "kolego.menu_title",
    icon: "mdi-account-details-outline",
    iconActive: "mdi-account-details",
    permission: "kolego.view_menu_rule",
  },
  children: [
    {
      path: "absences",
      component: () => import("./components/Absences.vue"),
      name: "kolego.absences",
      meta: {
        inMenu: true,
        titleKey: "kolego.absence.menu_title",
        icon: "mdi-account-clock-outline",
        iconActive: "mdi-account-clock",
        permission: "kolego.view_absences_rule",
      },
    },
    {
      path: "absence_reasons",
      component: () => import("./components/AbsenceReasons.vue"),
      name: "kolego.absence_reasons",
      meta: {
        inMenu: true,
        titleKey: "kolego.absence_reason.menu_title",
        icon: "mdi-tag-multiple-outline",
        iconActive: "mdi-tag-multiple",
        permission: "kolego.view_absencereasons_rule",
      },
    },
    {
      path: "absence_reason_tags",
      component: () => import("./components/AbsenceReasonTags.vue"),
      name: "kolego.absence_reason_tags",
      meta: {
        inMenu: true,
        titleKey: "kolego.absence_reason_tag.menu_title",
        icon: "mdi-tag-multiple-outline",
        iconActive: "mdi-tag-multiple",
        permission: "kolego.view_absencereasontags_rule",
      },
    },
  ],
};
