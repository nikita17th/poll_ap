<template>
  <div class="survey-view">
    <h1>Create Your Survey</h1>
    <SurveyCreator/>
  </div>
</template>

<script>
import SurveyCreator from '../components/SurveyCreator.vue';

export default {
  name: 'SurveyView',
  components: {
    SurveyCreator
  }
};
</script>

<style scoped>
.survey-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
  font-size: 2.5rem;
  color: #333;
  font-family: 'Roboto', sans-serif;
  font-weight: bold;
}

button {
  padding: 10px 20px;
  margin: 5px;
  background-color: #28a745;
  color: white;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease;
  text-align: center;
  display: inline-block;
}

button:hover {
  background-color: #218838;
  transform: translateY(-2px);
}

button:active {
  background-color: #1e7e34;
  transform: translateY(0);
}

input[type="text"] {
  padding: 10px;
  margin: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
  width: calc(50% - 20px);
  box-sizing: border-box;
}

::placeholder {
  color: #999;
}

option {
  padding: 10px;
}

select {
  padding: 10px;
  margin: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
  background-color: white;
}
</style>