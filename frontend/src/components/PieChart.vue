<template>
  <Pie :data="chartData" :options="options"
  />
</template>

<script>
import {Pie} from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, ArcElement } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, ArcElement);

export default {
  name: 'PieChart',
  components: {Pie},
  props: {
    externalData: {
      type: Object,
      required: true
    }
  },
  computed: {
    chartData() {
      return this.externalData;
    }
  },
  data() {
    return {
      chartOptions: {
        responsive: true
      }
    }
  }
}
</script>