<template>
  <div class="survey-results">
    <div v-if="!loading">
      <h2>{{ generalInfo.survey_title }}</h2>
      <h3>Count answers: {{ generalInfo.total_responses }}</h3>

      <div class="chart-container">
        <LineChart :externalData="timestampData" />
        <BarChart :externalData="cityData" />
      </div>

      <div v-for="question in questions" :key="question.id" class="question-block">
        <h3>{{ question.title }}</h3>

        <div v-if="['single', 'multiple'].includes(question.type)" class="chart-container">
          <BarChart :externalData="question.chartDataAnswers" />
          <PieChart :externalData="question.chartDataPercentages" />
        </div>

        <div v-else-if="question.type === 'text'" class="text-analysis">
          <h3>Average length answers: {{ question.average_text_length }}</h3>
          <BarChart :externalData="question.chartDataAnswers" />
          <PieChart :externalData="question.chartDataPercentages" />
        </div>
      </div>
      <div class="actions">
        <button @click="returnToHome">Back home</button>
      </div>
    </div>
    <div v-else class="loading-message">
      <p>loading...</p>
    </div>
  </div>
</template>

<script>
import LineChart from './LineChart.vue';
import BarChart from './BarChart.vue';
import PieChart from './PieChart.vue';

const colorPalette = [
  '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
  '#E7E9ED', '#F7464A', '#46BFBD', '#FDB45C', '#949FB1', '#4D5360',
  '#AC64AD', '#606060', '#54FF9F', '#43CD80', '#00FF7F', '#76EE00',
  '#008B8B', '#20B2AA', '#1E90FF', '#B22222', '#FFD700', '#32CD32',
  '#87CEEB', '#FF69B4', '#CD5C5C', '#8B8682', '#808000', '#556B2F'
];

export default {
  components: {LineChart, BarChart, PieChart},
  data() {
    return {
      jsonData: {
        general_info: {
          survey_title: undefined,
          total_responses: undefined,
          aggregated_timestamps: undefined,
          city_data: undefined,
        },
        question_stats: {
          answer_percentages: undefined,
          answers: undefined,
          top_3_text_responses: {
            percentage: undefined,
            response: undefined,
            count: undefined
          },
        }
      },
      loading: true
    };
  },

  created() {
    this.fetchData();
  },

  computed: {
    generalInfo() {
      return this.jsonData.general_info;
    },
    timestampData() {
      const labels = Object.keys(this.generalInfo.aggregated_timestamps);
      const counts = Object.values(this.generalInfo.aggregated_timestamps).map(entry => entry.count);
      return {
        labels,
        datasets: [{
          label: 'Count answers by day',
          backgroundColor: 'rgba(75,192,192,0.4)',
          borderColor: 'rgba(75,192,192,1)',
          data: counts
        }]
      }
    },
    cityData() {
      const labels = Object.keys(this.generalInfo.city_data);
      const data = Object.values(this.generalInfo.city_data);
      return {
        labels,
        datasets: [{
          label: 'Responses by City',
          backgroundColor: this.generateColors(labels.length),
          data: data
        }]
      }

    },

    questions() {
      return Object.entries(this.jsonData.question_stats).map(([id, question]) => {
            if (['single', 'multiple'].includes(question.type)) {
              const labelsPercentages = Object.keys(question.answer_percentages);
              const dataPercentages = Object.values(question.answer_percentages);
              const labelsAnswers = Object.keys(question.answers);const dataAnswers = Object.values(question.answers).map(answer => Number(answer));

              return {
                id,
                title: question.title,
                type: question.type,
                chartDataAnswers: {
                  labels: labelsAnswers,
                  datasets: [{
                    label: 'Answers',
                    backgroundColor: this.generateColors(labelsAnswers.length),
                    data: dataAnswers
                  }]
                },
                chartDataPercentages: {
                  labels: labelsPercentages,
                  datasets: [{
                    label: 'Answer Percentages',
                    backgroundColor: this.generateColors(labelsPercentages.length),
                    data: dataPercentages
                  }]
                },
                chartOptions: {
                  responsive: true,
                  maintainAspectRatio: false
                }
              };
            }
            const top_3_text_responses = question.top_3_text_responses
            const labels = top_3_text_responses.map(obj => obj.response)
            const percentages = top_3_text_responses.map(obj => obj.percentage);
            const counts = top_3_text_responses.map(obj => obj.count);
            return {
              id,
              title: question.title,
              type: question.type,
              average_text_length: question.average_text_length,
              chartDataAnswers: {
                labels: labels,
                datasets: [{
                  label: 'Answers',
                  backgroundColor: this.generateColors(labels.length),
                  data: counts
                }]
              },
              chartDataPercentages: {
                labels: labels,
                datasets: [{
                  label: 'Answer Percentages',
                  backgroundColor: this.generateColors(labels.length),
                  data: percentages
                }]
              },
              chartOptions: {
                responsive: true,
                maintainAspectRatio: false
              }
            };
          }
      )
    }
  },
  methods: {
    generateColors(count) {
      return Array.from({length: count}, (_, index) => {
        return colorPalette[index % colorPalette.length];
      });
    },
    async fetchData() {
      try {
        const surveyId = this.$route.params.id;
        const response = await this.$axios.get(`/survey/${surveyId}/responses`);
        this.jsonData = response.data;
      } catch (error) {
        if (error.response) {
          console.error('Error status:', error.response.status);
          console.error('Error data:', error.response.data);
        } else if (error.request) {
          console.error('No response received:', error.request);
        } else {
          console.error('Error:', error.message);
        }
      } finally {
        this.loading = false;
      }
    },
    returnToHome() {
      this.$router.push({name: 'Home'});
    },
  }
}
</script>


<style scoped>
.survey-results {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f4f7fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2, h3 {
  color: #333;
  text-align: center;
}

.chart-container {
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  justify-content: space-between;
  margin-bottom: 20px;
  padding: 10px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.question-block {
  margin-bottom: 30px;
}

.text-analysis {
  margin-top: 20px;
  background-color: #e2e8f0;
  padding: 15px;
  border-radius: 8px;
}

.loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
}

.actions {
  margin-top: 30px;
}

.actions button {
  display: inline-block;
  margin: 5px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
</style>