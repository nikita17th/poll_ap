import {createRouter, createWebHistory} from 'vue-router';
import Home from '../views/HomeView.vue';
import SurveyView from '../views/SurveyView.vue';
import SurveyParticipant from '../components/SurveyParticipant.vue';
import SurveyResults from '../components/SurveyResults.vue';
import SurveyConfirmation from "@/components/SurveyConfirmation.vue";

const routes = [
    {path: '/', name: 'Home', component: Home},
    {path: '/create-survey', name: 'CreateSurvey', component: SurveyView},
    {path: '/survey/:id', component: SurveyParticipant},
    {path: '/survey/:id/results', name: 'SurveyResults', component: SurveyResults},
    {path: '/survey-confirmation/:surveyId', name: 'SurveyConfirmation', component: SurveyConfirmation, props: true}
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
});

export default router;