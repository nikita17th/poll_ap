<template>
  <div class="survey-form">
    <h1>{{ survey.title }}</h1>
    <form @submit.prevent="submitSurvey">
      <div v-for="(question, index) in survey.questions" :key="question.id" class="question">
        <p class="question-text">{{ question.data.text }}</p>

        <div v-if="question.type === 'text'" class="input-group">
          <input v-model="responses[index].data" type="text" class="text-input" required/>
        </div>

        <div v-else-if="question.type === 'single'" class="input-group">
          <div v-for="(option, idx) in question.data.options" :key="idx" class="option">
            <input
                :name="'question-' + index"
                type="radio"
                :value="option"
                v-model="responses[index].data"
                required
            />
            <label>{{ option }}</label>
          </div>
        </div>

        <div v-else-if="question.type === 'multiple'" class="input-group">
          <div v-for="(option, idx) in question.data.options" :key="idx" class="option">
            <input
                type="checkbox"
                :value="option"
                v-model="responses[index].data"
            />
            <label>{{ option }}</label>
          </div>
        </div>
      </div>
      <button type="submit" class="submit-button">Submit</button>
    </form>
    <p v-if="submitted" class="thanks-message">Thank you for participating!</p>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>


<script>

export default {
  name: 'SurveyParticipant',
  data() {
    return {
      survey: {
        title: '',
        questions: []
      },
      responses: [],
      submitted: false,
      error: null
    };
  },
  created() {
    const surveyId = this.$route.params.id;
    this.$axios.get(`/survey/${surveyId}`)
        .then(response => {
          this.survey = response.data;
          this.responses = this.survey.questions.map(question => ({
            id: question.id,
            data: question.type === 'multiple' ? [] : ''
          }));
        })
        .catch(() => {
          this.error = 'There was a problem loading the survey. Please try again later.';
        });
  },
  methods: {
    async submitSurvey() {
      const surveyId = this.$route.params.id;
      const responsePayload = {
        responses: this.responses.map(response => ({
          id: response.id,
          data: response.data
        })),
        timestamp: new Date().toISOString()
      };
      try {
        await this.$axios.post(`/survey/${surveyId}/submit`, responsePayload);
        this.submitted = true;
        await this.$router.push({name: 'SurveyResults', params: {surveyId}});
      } catch (error) {
        console.error("Error submitting survey: ", error);
        alert(`Error where created survey ${JSON.stringify(error.response.data)} status ${error.status}`);
      }
    }
  }
};
</script>

<style scoped>
.survey-form {
  padding: 20px;
  max-width: 600px;
  margin: 0 auto;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h1 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.question {
  margin-bottom: 20px;
}

.question-text {
  font-size: 1.2rem;
  margin-bottom: 10px;
  color: #555;
}

.input-group {
  margin-bottom: 15px;
}

.text-input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.option {
  margin-bottom: 10px;
}

.submit-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.2s ease;
}

.submit-button:hover {
  background-color: #0056b3;
}

.thanks-message {
  margin-top: 20px;
  font-size: 1.2rem;
  color: #28a745;
  text-align: center;
}

.error-message {
  font-size: 1rem;
  color: red;
  text-align: center;
}
</style>