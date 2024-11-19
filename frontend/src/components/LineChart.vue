<template>
  <Line :data="chartData" :options="chartOptions"
  />
</template>

<script>
import {Line} from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale } from 'chart.js';

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, CategoryScale);

export default {
  name: 'LineChart',
  components: {Line},
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