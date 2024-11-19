<template>
  <div>
    <input type="text" v-model="localText" placeholder="Enter the question" @input="emitUpdate" />
  </div>
</template>


<script>
export default {
  props: {
    question: {
      type: Object,
      default: () => ({ text: ''})
    }
  },
  data() {
    return {
      localText: this.question.text || '',
    };
  },
  methods: {
    emitUpdate() {
      this.$emit('update-question', { text: this.localText });
    }
  },
  watch: {
    question: {
      handler(newQuestion) {
        this.localText = newQuestion.text;
      },
      deep: true
    }
  }

};
</script>

<style scoped>
input[type="text"],
textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 16px;
}

textarea {
  height: 60px;
  resize: vertical;
}
</style>