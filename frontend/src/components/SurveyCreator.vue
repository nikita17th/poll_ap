<template>
  <div class="survey-creator">
    <div class="button-group">
      <button @click="addQuestion('single')">Add Single Choice Question</button>
      <button @click="addQuestion('multiple')">Add Multiple Choice Question</button>
      <button @click="addQuestion('text')">Add Text Question</button>
    </div>

    <input
        type="text"
        v-model="title"
        placeholder="Enter survey title"
        class="survey-title-input"
    />

    <div v-for="(question, index) in questions" :key="question.id" class="question-box">
      <QuestionTypeSelector
          :question="question"
          :index="index"
          @update-question-type="updateQuestionType"
          @update-question-data="updateQuestionData"
      />
    </div>
    <button @click="submitSurvey" class="submit-button">Submit Survey</button>
  </div>
</template>
<script>
import QuestionTypeSelector from './QuestionTypeSelector.vue';

export default {
  components: {
    QuestionTypeSelector
  },
  data() {
    return {
      title: '',
      questions: [],
    };
  },
  methods: {
    generateUUID() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    },
    addQuestion(type) {
      let newQuestion = {
        id: this.generateUUID(),
        type: type,
        data: {
          text: '',
          options: type === 'text' ? [] : []
        }
      };
      this.questions.push(newQuestion);
    },
    updateQuestionType(type, index) {
      if (index >= 0 && index < this.questions.length) {
        this.questions[index].type = type;
        this.questions[index].data = {
          text: '',
          options: type === 'text' ? [] : []
        };
      } else {
        console.warn('Invalid index:', index);
      }
    },
    updateQuestionData(data, index) {
      if (index >= 0 && index < this.questions.length) {
        this.questions[index].data = data;
      } else {
        console.warn('Invalid index:', index);
      }
    },
    async submitSurvey() {
      try {
        const surveyData = {
          title: this.title,
          timestamp: new Date().toISOString(),
          questions: this.questions.map(q => ({
            id: q.id,
            type: q.type,
            data: q.data
          })),
        };
        const response = await this.$axios.post(`/surveys`, surveyData);
        const surveyId = response.data.id;
        await this.$router.push({name: 'SurveyConfirmation', params: {surveyId}});
      } catch (error) {
        console.error('Error crete survey:', error);
        alert(`Error where created survey ${JSON.stringify(error.response.data)} status ${error.status}`);
      }
    }
  }
};
</script>

<style scoped>
.survey-creator {
  padding: 20px;
  margin: 0 auto;
  max-width: 800px;
  background-color: #f8f9fa;
  border-radius: 8px;
  font-family: 'Roboto', sans-serif;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.5rem;
  color: #333;
}

.button-group {
  display: flex;
  justify-content: space-around;
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  margin: 5px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  font-family: 'Roboto', sans-serif;
  transition: background-color 0.3s ease, transform 0.3s ease;
}

button:hover {
  background-color: #218838;
  transform: translateY(-2px);
}

button:active {
  background-color: #1e7e34;
  transform: translateY(0);
}

.survey-title-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.question-box {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  background-color: #fff;
  font-family: 'Roboto', sans-serif;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.submit-button {
  width: 100%;
  background-color: #007bff;
}

.submit-button:hover {
  background-color: #0056b3;
}

.submit-button:active {
  background-color: #004085;
}
</style>