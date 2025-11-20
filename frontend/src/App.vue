<template>
  <div class="min-h-screen bg-[#020617] text-slate-100 relative overflow-hidden selection:bg-blue-500 selection:text-white">
    <!-- Aurora glows -->
    <div class="pointer-events-none fixed top-[-6rem] left-1/4 h-96 w-96 rounded-full bg-blue-500/25 blur-[140px]"></div>
    <div class="pointer-events-none fixed bottom-[-6rem] right-1/4 h-96 w-96 rounded-full bg-purple-500/25 blur-[140px]"></div>

    <div class="relative z-10 mx-auto max-w-7xl px-6 py-10">
      <header class="mb-10 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p class="text-xs uppercase tracking-[0.25em] text-slate-500">Real-time auction lab</p>
          <h1 class="bg-gradient-to-r from-blue-400 via-cyan-300 to-violet-400 bg-clip-text text-4xl font-bold tracking-tight text-transparent">
            AdEcon Dashboard
          </h1>
          <p class="mt-2 text-slate-400">Run GSP/VCG simulations with ONNX inference and see revenue dynamics instantly.</p>
        </div>
        <div class="flex items-center gap-3">
          <span class="rounded-full bg-white/5 px-3 py-1 text-xs font-semibold text-cyan-300 border border-white/10 backdrop-blur-md shadow-lg shadow-cyan-500/10">
            DeepFM · ONNX · Feast
          </span>
          <div class="flex items-center gap-2 rounded-full bg-white/5 px-3 py-1 text-sm text-green-300 border border-white/10 backdrop-blur-md shadow-lg shadow-emerald-500/10">
            <span class="h-2 w-2 rounded-full bg-green-400 animate-pulse"></span>
            System online
          </div>
        </div>
      </header>

      <div class="grid grid-cols-12 gap-6">
        <!-- Configuration Panel -->
        <section class="col-span-12 lg:col-span-4 space-y-4 rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl backdrop-blur-xl">
          <div class="flex items-center justify-between">
            <h2 class="text-xl font-semibold text-slate-50 flex items-center gap-2">
              <span class="text-blue-300">⚙️</span> Configuration
            </h2>
            <span class="text-xs text-slate-400">Interactive · Live</span>
          </div>

          <div class="space-y-4">
            <div>
              <label class="text-xs font-semibold uppercase tracking-wider text-slate-400">User ID</label>
              <input
                v-model="userId"
                class="mt-2 w-full rounded-2xl border border-white/10 bg-black/30 px-4 py-3 text-sm text-white outline-none transition focus:border-blue-500/60 focus:ring-2 focus:ring-blue-500/30"
                placeholder="dev_412"
              />
            </div>

            <div>
              <label class="text-xs font-semibold uppercase tracking-wider text-slate-400">Mechanism</label>
              <div class="mt-2 flex rounded-2xl bg-black/30 p-1.5 border border-white/10">
                <button
                  @click="mechanism='gsp'"
                  :class="['flex-1 rounded-xl py-2 text-sm font-semibold transition-all duration-300', mechanism==='gsp' ? 'bg-white/10 text-white shadow-lg shadow-blue-500/20 border border-white/5' : 'text-slate-500 hover:text-slate-300']">
                  GSP
                </button>
                <button
                  @click="mechanism='vcg'"
                  :class="['flex-1 rounded-xl py-2 text-sm font-semibold transition-all duration-300', mechanism==='vcg' ? 'bg-white/10 text-white shadow-lg shadow-violet-500/20 border border-white/5' : 'text-slate-500 hover:text-slate-300']">
                  VCG
                </button>
              </div>
            </div>

            <div class="space-y-3">
              <div class="flex items-center justify-between text-xs font-semibold uppercase tracking-wider text-slate-400">
                <span>Candidates</span>
                <span class="text-slate-500">{{ candidates.length }} ads</span>
              </div>

              <div class="space-y-2">
                <div v-for="(cand, index) in candidates" :key="index" class="flex items-center gap-3 rounded-xl border border-white/5 bg-white/5 px-3 py-3 backdrop-blur-md">
                  <input
                    v-model="cand.ad_id"
                    class="w-28 rounded-lg border border-white/10 bg-black/30 px-3 py-2 text-sm text-white outline-none transition focus:border-blue-500/60 focus:ring-1 focus:ring-blue-500/30"
                    placeholder="Ad ID"
                  />
                  <input
                    v-model.number="cand.bid"
                    type="number"
                    step="0.1"
                    class="w-24 rounded-lg border border-white/10 bg-black/30 px-3 py-2 text-sm text-white outline-none transition focus:border-blue-500/60 focus:ring-1 focus:ring-blue-500/30"
                    placeholder="Bid"
                  />
                  <button @click="removeCandidate(index)" class="ml-auto text-slate-500 transition hover:text-red-400">
                    ✕
                  </button>
                </div>
              </div>

              <button
                @click="addCandidate"
                class="w-full rounded-xl border border-dashed border-white/20 bg-white/5 py-2 text-sm font-semibold text-slate-200 transition hover:border-blue-400/50 hover:text-white">
                + Add candidate
              </button>
            </div>

            <button
              @click="runAuction"
              :disabled="loading"
              class="w-full rounded-2xl bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 py-3 text-sm font-bold text-white shadow-xl shadow-blue-900/30 transition hover:from-blue-500 hover:to-purple-500 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-60">
              {{ loading ? 'Running simulation...' : 'Run auction simulation' }}
            </button>
          </div>
        </section>

        <!-- Results Panel -->
        <section class="col-span-12 space-y-6 lg:col-span-8">
          <div v-if="results.length > 0" class="space-y-6">
            <div class="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl backdrop-blur-xl">
              <div class="mb-4 flex items-center justify-between">
                <h2 class="text-lg font-semibold text-slate-50">Auction dynamics</h2>
                <span class="rounded-full border border-emerald-400/30 bg-emerald-500/15 px-3 py-1 text-xs font-semibold text-emerald-200 backdrop-blur-md">
                  Live
                </span>
              </div>
              <MechanismChart :results="results" />
            </div>

            <div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
              <div v-for="res in results" :key="res.ad_id">
                <AdCard :ad="res" />
              </div>
            </div>
          </div>

          <div v-else class="flex h-80 flex-col items-center justify-center rounded-3xl border border-dashed border-white/15 bg-white/5 text-slate-400 backdrop-blur-xl">
            <p class="text-lg text-slate-200">No results yet</p>
            <p class="text-sm text-slate-500">Run the simulation to see auction outcomes.</p>
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
