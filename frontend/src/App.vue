<template>
  <div class="min-h-screen bg-slate-50 p-8 font-sans text-slate-800">
    
    <div class="mx-auto max-w-6xl">
      <header class="mb-8 text-center">
        <h1 class="text-3xl font-bold tracking-tight text-slate-900">AdEcon Dashboard</h1>
        <p class="text-slate-500">Real-time Auction Simulation & Analytics</p>
      </header>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
        
        <!-- Configuration Panel -->
        <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm h-fit">
          <h2 class="mb-4 text-lg font-semibold">Settings</h2>
          
          <div class="mb-4">
            <label class="mb-1 block text-sm font-medium text-slate-600">User ID</label>
            <input 
              v-model="userId" 
              class="w-full rounded-lg border border-slate-200 bg-slate-50 px-4 py-2 text-sm focus:border-indigo-500 focus:ring-2 focus:ring-indigo-200 transition-all outline-none"
              placeholder="e.g. user_123"
            />
          </div>

          <div class="mb-6">
            <label class="mb-1 block text-sm font-medium text-slate-600">Mechanism</label>
            <div class="flex rounded-lg bg-slate-100 p-1">
              <button 
                @click="mechanism='gsp'"
                :class="['flex-1 rounded-md py-1.5 text-sm font-medium transition-all', mechanism==='gsp' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700']"
              >
                GSP
              </button>
              <button 
                @click="mechanism='vcg'"
                :class="['flex-1 rounded-md py-1.5 text-sm font-medium transition-all', mechanism==='vcg' ? 'bg-white text-indigo-600 shadow-sm' : 'text-slate-500 hover:text-slate-700']"
              >
                VCG
              </button>
            </div>
          </div>

          <div class="mb-4">
            <label class="mb-1 block text-sm font-medium text-slate-600">Candidates</label>
            <div v-for="(cand, index) in candidates" :key="index" class="flex items-center gap-2 mb-2">
              <input v-model="cand.ad_id" class="w-24 rounded-lg border border-slate-200 bg-slate-50 px-2 py-1 text-sm outline-none focus:border-indigo-500" placeholder="Ad ID" />
              <input v-model.number="cand.bid" type="number" step="0.1" class="w-20 rounded-lg border border-slate-200 bg-slate-50 px-2 py-1 text-sm outline-none focus:border-indigo-500" placeholder="Bid" />
              <button @click="removeCandidate(index)" class="text-slate-400 hover:text-red-500 transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-5 h-5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </button>
            </div>
            <button @click="addCandidate" class="mt-2 w-full rounded-lg border border-dashed border-slate-300 py-2 text-sm text-slate-500 hover:border-indigo-500 hover:text-indigo-600 transition-colors">
              + Add Candidate
            </button>
          </div>

          <button 
            @click="runAuction" 
            :disabled="loading"
            class="w-full rounded-lg bg-indigo-600 py-2.5 text-sm font-semibold text-white shadow-md hover:bg-indigo-500 transition-colors active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? 'Running...' : 'Run Auction Simulation' }}
          </button>
        </div>

        <!-- Results Panel -->
        <div class="lg:col-span-2 space-y-6">
          <div v-if="results.length > 0">
            <div class="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
              <div class="mb-4 flex items-center justify-between">
                <h2 class="text-lg font-semibold">Auction Dynamics</h2>
                <span class="rounded-full bg-green-100 px-2.5 py-0.5 text-xs font-medium text-green-700">Live</span>
              </div>
              <MechanismChart :results="results" />
            </div>
            
            <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3 mt-6">
               <div v-for="res in results" :key="res.ad_id">
                 <AdCard :ad="res" />
               </div>
            </div>
          </div>
          
          <div v-else class="flex h-64 items-center justify-center rounded-xl border border-dashed border-slate-300 bg-slate-50 text-slate-400">
            <div class="text-center">
              <p>No results yet.</p>
              <p class="text-sm">Run the simulation to see auction outcomes.</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import AdCard from './components/AdCard.vue';
import MechanismChart from './components/MechanismChart.vue';
import { ElMessage } from 'element-plus';

const userId = ref('dev_412');
const mechanism = ref('gsp');
const candidates = ref([
  { ad_id: 'ad_1', bid: 1.5 },
  { ad_id: 'ad_2', bid: 2.0 },
  { ad_id: 'ad_3', bid: 0.5 },
  { ad_id: 'ad_4', bid: 1.2 }
]);
const results = ref([]);
const loading = ref(false);

const addCandidate = () => {
  candidates.value.push({ ad_id: `ad_${candidates.value.length + 1}`, bid: 1.0 });
};

const removeCandidate = (index) => {
  candidates.value.splice(index, 1);
};

const runAuction = async () => {
  loading.value = true;
  try {
    const response = await axios.post('http://localhost:8000/recommend', {
      user_id: userId.value,
      candidates: candidates.value,
      mechanism: mechanism.value
    });
    results.value = response.data.results;
    ElMessage.success('Auction completed successfully');
  } catch (error) {
    console.error(error);
    ElMessage.error('Failed to run auction: ' + error.message);
  } finally {
    loading.value = false;
  }
};
</script>

<style>
/* Global styles are now in style.css */
</style>
