<template>
  <div>
    <select v-model="localQuestionType" @change="changeQuestionType">
      <option value="single">Single Choice</option>
      <option value="multiple">Multiple Choice</option>
      <option value="text">Text</option>
    </select>

    <component :is="currentComponent" :question="questionData" @update-question="updateQuestionData"></component>
  </div>
</template>

<script>
import SingleChoiceQuestion from './SingleChoiceQuestion.vue';
import MultipleChoiceQuestion from './MultipleChoiceQuestion.vue';
import TextQuestion from './TextQuestion.vue';

export default {
  components: {
    SingleChoiceQuestion,
    MultipleChoiceQuestion,
    TextQuestion
  },
  props: {
    question: {
      type: Object,
      required: true
    },
    index: {
      type: Number,
      required: true
    }
  }
,
  data() {
    return {
      localQuestionType: this.question.type || 'single',
      questionData: {...this.question.data}
    };
  },
  computed: {
    currentComponent() {
      switch (this.localQuestionType) {
        case 'single':
          return 'SingleChoiceQuestion';
        case 'multiple':
          return 'MultipleChoiceQuestion';
        case 'text':
          return 'TextQuestion';
        default:
          return null;
      }
    }
  },
  methods: {
    changeQuestionType() {
      this.$emit('update-question-type', this.localQuestionType, this.index);
      switch (this.localQuestionType) {
        case 'single':
          this.questionData = { text: '', options: [] };
          break;
        case 'multiple':
          this.questionData = { text: '', options: [] };
          break;
        case 'text':
          this.questionData = { text: '' };
          break;
        default:
          this.questionData = {};
      }
      this.$emit('update-question-data', this.questionData, this.index);
    },
    updateQuestionData(updatedData) {
      this.$emit('update-question-data', updatedData, this.index);
    }
  }

  ,
  watch: {
    question: {
      handler(newValue) {
        this.localQuestionType = newValue.type;
        this.questionData = {...newValue.data};
      },
      deep: true
    }
  }
};
</script>

<style scoped>
/* Стили вашего компонента */
</style>