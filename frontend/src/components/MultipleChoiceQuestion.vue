<template>
  <div>
    <input type="text" v-model="localQuestion.text" placeholder="Enter the question" />
    <div v-for="(option, index) in localQuestion.options" :key="index" class="option">
      <input type="text" v-model="localQuestion.options[index]" placeholder="Option" />
      <button @click="removeOption(index)">Remove</button>
    </div>
    <button @click="addOption">Add Option</button>
  </div>
</template>

<script>
export default {
  props: {
    question: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localQuestion: {
        text: this.question.text || '',
        options: [ ...this.question.options ] || ['']
      }
    };
  },
  watch: {
    localQuestion: {
      handler(val) {
        this.$emit('update-question', val);
      },
      deep: true
    }
  },
  methods: {
    addOption() {
      this.localQuestion.options.push('');
    },
    removeOption(index) {
      this.localQuestion.options.splice(index, 1);
    }
  }
};
</script>

<style scoped>
.option {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

input[type="text"] {
  flex: 1;
  margin-right: 10px;
}

button {
  background-color: #f56b6b;
  border: none;
  color: white;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  background-color: #c44545;
}
</style>