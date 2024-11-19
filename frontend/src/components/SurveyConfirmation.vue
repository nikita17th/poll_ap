<template>
  <div class="survey-confirmation">
    <h2>Survey Created!</h2>
    <p class="survey-id">ID Survey: {{ surveyId }}</p>

    <div class="link-row">
      <div class="link-section">
        <a :href="surveyUrl" target="_blank" class="link-button">Take the survey</a>
        <button @click="copyToClipboard(surveyUrl)" class="copy-button">Copy URL</button>
      </div>
      <div class="qr-code-section">
        <canvas ref="qrCanvasSurvey" class="qr-canvas"></canvas>
      </div>
    </div>

    <div class="link-row">
      <div class="link-section">
        <a :href="resultsUrl" target="_blank" class="link-button">View results</a>
        <button @click="copyToClipboard(resultsUrl)" class="copy-button">Copy URL</button>
      </div>
      <div class="qr-code-section">
        <canvas ref="qrCanvasResults" class="qr-canvas"></canvas>
      </div>
    </div>

    <div class="actions">
      <button @click="returnToHome">Back home</button>
    </div>
  </div>
</template>




<script>
import QRCode from 'qrcode'

export default {
  props: ['surveyId'],
  computed: {
    surveyUrl() {
      return `${this.$baseUrl}/survey/${this.surveyId}`;
    },
    resultsUrl() {
      return `${this.$baseUrl}/survey/${this.surveyId}/results`;
    }
  },
  mounted() {
    this.generateQRCode(this.surveyUrl, this.$refs.qrCanvasSurvey);
    this.generateQRCode(this.resultsUrl, this.$refs.qrCanvasResults);
  },
  methods: {
    copyToClipboard(url) {
      const tempInput = document.createElement('input');
      document.body.appendChild(tempInput);
      tempInput.value = url;
      tempInput.select();

      try {
        document.execCommand('copy');
        alert('URL copied!');
      } catch (err) {
        console.error('Error copying URL:', err);
      }

      document.body.removeChild(tempInput);
    },
    openInNewTab(url) {
      window.open(url, '_blank');
    },
    returnToHome() {
      this.$router.push({name: 'Home'});
    },
    generateQRCode(url, canvasElement) {
      QRCode.toCanvas(canvasElement, url, error => {
        if (error) console.error('Error generation QR-code:', error);
      });
    }
  }
};
</script>
<style scoped>
.survey-confirmation {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
  font-family: 'Roboto', sans-serif;
}

.survey-id {
  font-style: italic;
  color: #555;
  margin-bottom: 20px;
  font-family: 'Roboto', sans-serif;
}

.link-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
  font-family: 'Roboto', sans-serif;
}

.link-section {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  font-family: 'Roboto', sans-serif;
}

.link-button, .copy-button {
  margin: 5px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-decoration: none;
  transition: background-color 0.2s ease;
  font-family: 'Roboto', sans-serif;
}

.link-button:hover, .copy-button:hover {
  background-color: #0056b3;
}

.qr-code-section {
  width: 150px;
}

.qr-canvas {
  width: 100%;
  height: auto;
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
  font-family: 'Roboto', sans-serif;
}

.actions button:hover {
  background-color: #0056b3;
}
</style>