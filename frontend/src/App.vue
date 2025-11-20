<template>
  <div class="min-h-screen bg-gray-50 font-sans text-slate-600 selection:bg-indigo-100 selection:text-indigo-700">
    <div class="mx-auto max-w-6xl px-6 py-10">
      <header class="mb-10 flex flex-col gap-4 border-b border-gray-200 pb-6 md:flex-row md:items-end md:justify-between">
        <div>
          <h1 class="text-3xl font-semibold tracking-tight text-slate-900">AdEcon Simulation</h1>
          <p class="mt-2 text-sm text-slate-500">Real-time advertising auction dynamics & revenue analysis.</p>
        </div>
        <div class="flex items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1 text-xs font-medium text-emerald-600">
          <span class="relative flex h-2 w-2">
            <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span>
            <span class="relative inline-flex h-2 w-2 rounded-full bg-emerald-500"></span>
          </span>
          Live connected
        </div>
      </header>

      <div class="grid grid-cols-1 gap-8 lg:grid-cols-12">
        <!-- Configuration -->
        <section class="space-y-6 rounded-xl border border-gray-100 bg-white p-6 shadow-[0_2px_8px_rgba(0,0,0,0.04)] lg:col-span-4">
          <h2 class="text-sm font-semibold uppercase tracking-wider text-slate-900">Configuration</h2>

          <div class="space-y-5">
            <div>
              <label class="mb-1.5 block text-xs font-medium text-slate-500">User identity</label>
              <input
                v-model="userId"
                class="w-full rounded-lg border-0 bg-gray-50 px-4 py-3 text-sm text-slate-900 ring-1 ring-inset ring-gray-200 transition-all placeholder:text-gray-400 focus:bg-white focus:ring-2 focus:ring-indigo-600"
                placeholder="Identifier..."
              />
            </div>

            <div>
              <label class="mb-1.5 block text-xs font-medium text-slate-500">Auction mechanism</label>
              <div class="grid grid-cols-2 gap-1 rounded-lg bg-gray-100/60 p-1">
                <button
                  @click="mechanism='gsp'"
                  :class="['rounded-md py-2 text-xs font-medium transition-all', mechanism==='gsp' ? 'bg-white text-slate-900 shadow-sm ring-1 ring-gray-200' : 'text-slate-500 hover:text-slate-700']">
                  GSP (Second Price)
                </button>
                <button
                  @click="mechanism='vcg'"
                  :class="['rounded-md py-2 text-xs font-medium transition-all', mechanism==='vcg' ? 'bg-white text-slate-900 shadow-sm ring-1 ring-gray-200' : 'text-slate-500 hover:text-slate-700']">
                  VCG (Welfare)
                </button>
              </div>
            </div>

            <div class="space-y-3">
              <div class="flex items-center justify-between text-xs font-medium text-slate-500">
                <span>Candidates</span>
                <span class="text-slate-400">{{ candidates.length }} ads</span>
              </div>

              <div class="space-y-2">
                <div v-for="(cand, index) in candidates" :key="index" class="flex items-center gap-3 rounded-lg border border-gray-100 bg-gray-50 px-3 py-3">
                  <input
                    v-model="cand.ad_id"
                    class="w-28 rounded-md border-0 bg-white px-3 py-2 text-sm text-slate-900 ring-1 ring-gray-200 transition focus:ring-2 focus:ring-indigo-500"
                    placeholder="Ad ID"
                  />
                  <input
                    v-model.number="cand.bid"
                    type="number"
                    step="0.1"
                    class="w-24 rounded-md border-0 bg-white px-3 py-2 text-sm text-slate-900 ring-1 ring-gray-200 transition focus:ring-2 focus:ring-indigo-500"
                    placeholder="Bid"
                  />
                  <button @click="removeCandidate(index)" class="ml-auto text-slate-400 transition hover:text-red-500">✕</button>
                </div>
              </div>

              <button
                @click="addCandidate"
                class="w-full rounded-lg border border-dashed border-gray-200 bg-white py-2 text-sm font-medium text-slate-600 transition hover:border-indigo-200 hover:text-indigo-700">
                + Add candidate
              </button>
            </div>

            <button
              @click="runAuction"
              :disabled="loading"
              class="group relative w-full overflow-hidden rounded-lg bg-slate-900 px-4 py-3 text-sm font-semibold text-white shadow-md transition hover:bg-slate-800 hover:shadow-lg active:translate-y-[1px] disabled:cursor-not-allowed disabled:opacity-60">
              <span class="relative z-10 flex items-center justify-center gap-2">
                {{ loading ? 'Running…' : 'Run auction' }}
                <svg class="h-4 w-4 text-slate-300 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
              </span>
            </button>
          </div>
        </section>

        <!-- Results -->
        <section class="space-y-6 lg:col-span-8">
          <div v-if="results.length > 0" class="space-y-6">
            <div class="rounded-xl border border-gray-100 bg-white p-6 shadow-[0_2px_8px_rgba(0,0,0,0.04)]">
              <div class="mb-6 flex items-center justify-between">
                <h3 class="text-base font-medium text-slate-900">Auction dynamics</h3>
                <div class="flex gap-4 text-xs text-slate-500">
                  <span class="flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-indigo-500"></span>Cost (CPC)</span>
                  <span class="flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-slate-300"></span>Surplus</span>
                </div>
              </div>
              <MechanismChart :results="results" />
            </div>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              <div v-for="res in results" :key="res.ad_id">
                <AdCard :ad="res" />
              </div>
            </div>
          </div>

          <div v-else class="flex h-72 flex-col items-center justify-center rounded-xl border border-dashed border-gray-200 bg-white text-slate-500">
            <p class="text-base font-medium text-slate-700">No results yet</p>
            <p class="text-sm mt-1">Run the simulation to see auction outcomes.</p>
          </div>
        </section>
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
