<template>
  <div class="home">
    <h1>Welcome to the Survey Creator</h1>
    <p>Create custom surveys easily and efficiently.</p>
    <router-link to="/create-survey">
      <button>Create a New Survey</button>
    </router-link>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
};
</script>

<style scoped>
.home {
  text-align: center;
  margin-top: 50px;
}

button {
  background-color: #42b983;
  border: none;
  color: white;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border-radius: 4px;
}

button:hover {
  background-color: #358a62;
}
</style>