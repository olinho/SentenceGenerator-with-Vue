export default {
  name: 'inflection',
  // REMEMBER: declare data properties as function to be reactive
  data() {
    return {};
  },
  props: ['description'],
  template: '<td v-if="description.czesc_mowy === 0">{{ description.deklinacja }}</td>' +
  '<td v-else-if="description.czesc_mowy === 1">{{ description.koniugacja }}</td>' +
  '<td v-else-if="description.czesc_mowy === 2">{{ description.deklinacja }}</td>' +
  '<td v-else></td>',
}
