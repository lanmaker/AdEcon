<template>
  <div
    class="min-h-screen bg-slate-50 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-100 via-slate-50 to-slate-50 p-6 font-sans text-slate-600 selection:bg-indigo-500 selection:text-white"
  >
    <div class="mx-auto max-w-7xl">
      <header class="mb-6 flex flex-col gap-4 border-b border-slate-200 pb-6 md:flex-row md:items-center md:justify-between">
        <div>
          <h1 class="text-2xl font-bold tracking-tight text-slate-900">
            AdEcon <span class="font-light text-slate-400">Simulation</span>
          </h1>
          <p class="mt-1 flex items-center gap-2 text-sm text-slate-500">
            Real-time auction dynamics & revenue analysis
            <span class="h-1 w-1 rounded-full bg-slate-300"></span>
            <span class="font-mono text-xs text-slate-400">v2</span>
          </p>
        </div>

        <div class="flex flex-wrap gap-2">
          <div
            class="hidden items-center gap-2 rounded-full border px-3 py-1.5 text-xs font-medium shadow-sm md:flex"
            :class="backendReady ? 'border-emerald-200 bg-emerald-50 text-emerald-700' : 'border-rose-200 bg-rose-50 text-rose-700'"
          >
            <span class="h-1.5 w-1.5 rounded-full" :class="backendReady ? 'bg-emerald-400' : 'bg-rose-400'"></span>
            {{ backendStatusLabel }}
          </div>
          <div class="flex items-center gap-2 rounded-full border border-slate-200 bg-white px-3 py-1.5 text-xs font-medium text-slate-600 shadow-sm">
            <span class="text-slate-400">Model:</span>
            <span class="font-mono text-slate-800">{{ modelStatusLabel }}</span>
          </div>
        </div>
      </header>

      <div
        v-if="errorMessage"
        class="mb-4 rounded-lg border border-rose-200 bg-rose-50 px-4 py-3 text-sm text-rose-700"
      >
        {{ errorMessage }}
      </div>

      <!-- Metrics strip -->
      <div class="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div class="rounded-lg border border-slate-200 bg-white px-4 py-3 shadow-sm">
          <p class="text-xs font-medium uppercase tracking-wide text-slate-500">Active bidders</p>
          <p class="mt-2 text-2xl font-semibold text-slate-900">{{ summary.activeBidders }}</p>
        </div>
        <div class="rounded-lg border border-slate-200 bg-white px-4 py-3 shadow-sm">
          <p class="text-xs font-medium uppercase tracking-wide text-slate-500">Avg pCTR</p>
          <p class="mt-2 font-mono text-xl font-semibold text-slate-900">{{ summary.avgPctr }}%</p>
        </div>
        <div class="rounded-lg border border-slate-200 bg-white px-4 py-3 shadow-sm">
          <p class="text-xs font-medium uppercase tracking-wide text-slate-500">Total cost</p>
          <p class="mt-2 font-mono text-xl font-semibold text-slate-900">${{ summary.totalCost }}</p>
        </div>
        <div class="rounded-lg border border-slate-200 bg-white px-4 py-3 shadow-sm">
          <p class="text-xs font-medium uppercase tracking-wide text-slate-500">Latency</p>
          <p class="mt-2 text-xl font-semibold text-slate-900">{{ latencyLabel }}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
        <!-- Configuration -->
        <section class="lg:col-span-4">
          <div class="sticky top-6 overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm transition-all hover:shadow-md">
            <div class="flex items-center justify-between border-b border-slate-100 bg-slate-50/60 px-5 py-3">
              <h2 class="text-xs font-semibold uppercase tracking-wider text-slate-600">Configuration</h2>
              <svg class="h-4 w-4 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
                />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>

            <div class="space-y-6 p-5">
              <div class="group">
                <label class="mb-1.5 block text-[11px] font-bold uppercase text-slate-400 transition-colors group-focus-within:text-indigo-600">
                  Target user identity
                </label>
                <div class="relative">
                  <span class="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">
                    <svg class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                  </span>
                  <input
                    v-model="userId"
                    class="w-full rounded-md border border-slate-200 bg-slate-50 py-2.5 pl-9 pr-3 text-sm font-mono text-slate-900 transition-all placeholder:text-slate-400 focus:border-indigo-500 focus:bg-white focus:outline-none focus:ring-1 focus:ring-indigo-500"
                    placeholder="user_id"
                  />
                </div>
              </div>

              <div>
                <label class="mb-1.5 block text-[11px] font-bold uppercase text-slate-400">Auction logic</label>
                <div class="grid grid-cols-2 gap-1 rounded-lg border border-slate-200 bg-slate-100 p-1">
                  <button
                    @click="mechanism='gsp'"
                    :class="[
                      'flex items-center justify-center gap-2 rounded-md py-2 text-xs font-semibold transition-all',
                      mechanism==='gsp' ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-slate-200' : 'text-slate-500 hover:text-slate-900'
                    ]"
                  >
                    GSP <span class="text-[10px] font-normal opacity-50">2nd price</span>
                  </button>
                  <button
                    @click="mechanism='vcg'"
                    :class="[
                      'flex items-center justify-center gap-2 rounded-md py-2 text-xs font-semibold transition-all',
                      mechanism==='vcg' ? 'bg-white text-indigo-600 shadow-sm ring-1 ring-slate-200' : 'text-slate-500 hover:text-slate-900'
                    ]"
                  >
                    VCG <span class="text-[10px] font-normal opacity-50">Welfare</span>
                  </button>
                </div>
              </div>

              <div class="space-y-2">
                <label class="mb-1.5 flex justify-between text-[11px] font-bold uppercase text-slate-400">
                  <span>Bidding candidates</span>
                  <button class="text-indigo-500 hover:underline" @click="addCandidate" type="button">+ Add</button>
                </label>

                <div
                  v-for="(ad, idx) in candidates"
                  :key="idx"
                  class="group flex items-center gap-2 rounded-md border border-slate-100 bg-white p-1.5 shadow-sm transition-colors hover:border-indigo-100"
                >
                  <div class="flex h-8 w-8 items-center justify-center rounded bg-slate-100 font-mono text-xs font-bold text-slate-500">{{ idx + 1 }}</div>
                  <input
                    v-model="ad.ad_id"
                    class="min-w-0 flex-1 bg-transparent text-sm font-medium text-slate-700 focus:outline-none"
                    placeholder="ad_id"
                  />
                  <div class="flex items-center gap-1 rounded border border-slate-100 bg-slate-50 px-2 py-1">
                    <span class="text-xs text-slate-400">$</span>
                    <input
                      v-model.number="ad.bid"
                      type="number"
                      step="0.1"
                      class="w-16 bg-transparent text-right text-sm font-mono text-slate-900 focus:outline-none"
                      placeholder="bid"
                    />
                  </div>
                  <button class="p-1 text-slate-300 transition-opacity hover:text-rose-500 group-hover:opacity-100 opacity-0" @click="removeCandidate(idx)" type="button">
                    ×
                  </button>
                </div>
              </div>

              <button
                @click="runAuction"
                :disabled="loading"
                class="relative w-full overflow-hidden rounded-lg bg-indigo-600 px-4 py-3.5 text-sm font-semibold text-white shadow-md transition hover:-translate-y-0.5 hover:shadow-lg active:translate-y-0 disabled:cursor-not-allowed disabled:opacity-60"
              >
                <div class="absolute inset-0 bg-white/10 opacity-0 transition-opacity hover:opacity-100"></div>
                <span class="relative z-10 flex items-center justify-center gap-2">
                  {{ loading ? 'Running…' : 'Run simulation' }}
                  <svg class="h-4 w-4 text-indigo-100 transition-transform group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
                  </svg>
                </span>
              </button>
            </div>
          </div>
        </section>

        <!-- Results -->
        <section class="space-y-6 lg:col-span-8">
          <div class="relative flex h-[420px] flex-col rounded-xl border border-slate-200 bg-white shadow-sm">
            <div class="flex items-center justify-between border-b border-slate-100 px-6 py-4">
              <div>
                <h3 class="font-semibold text-slate-900">Auction dynamics</h3>
                <p class="text-xs text-slate-500">Real-time bid vs. payment analysis</p>
              </div>
              <div class="flex gap-4 text-xs font-medium text-slate-500">
                <span class="flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-indigo-500"></span>Cost (CPC)</span>
                <span class="flex items-center gap-1.5"><span class="h-2 w-2 rounded-full bg-slate-300"></span>Surplus</span>
              </div>
            </div>

            <div class="relative flex-1 p-4">
              <div v-if="!hasData" class="absolute inset-0 flex flex-col items-center justify-center bg-slate-50/70">
                <div class="mb-2 text-slate-300">
                  <svg class="h-12 w-12 opacity-60" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <p class="text-sm font-medium text-slate-500">Ready to simulate</p>
                <p class="mt-1 text-xs text-slate-400">Configure candidates and run to view analytics</p>
              </div>
              <div v-else class="h-full w-full">
                <MechanismChart :results="results" />
              </div>
            </div>
          </div>

          <div class="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm">
            <div class="overflow-x-auto">
              <table class="min-w-[680px] w-full text-left text-sm">
              <thead class="border-b border-slate-100 bg-slate-50 text-xs uppercase text-slate-500">
                <tr>
                  <th class="px-6 py-3 font-semibold">Ad candidate</th>
                  <th class="px-6 py-3 text-right font-semibold">pCTR</th>
                  <th class="px-6 py-3 text-right font-semibold">Bid</th>
                  <th class="px-6 py-3 text-right font-semibold">Cost</th>
                  <th class="px-6 py-3 text-right font-semibold">Surplus</th>
                </tr>
              </thead>
              <tbody v-if="hasData" class="divide-y divide-slate-100">
                <tr v-for="ad in results" :key="ad.ad_id" class="transition-colors hover:bg-slate-50/80">
                  <td class="px-6 py-4 font-medium text-slate-900">
                    <span
                      :class="['mr-2 inline-block h-2 w-2 rounded-full', ad.rank === 1 ? 'bg-indigo-500' : 'bg-slate-300']"
                    ></span>
                    {{ ad.ad_id }}
                  </td>
                  <td class="px-6 py-4 text-right font-mono text-slate-700">{{ (ad.pctr * 100).toFixed(2) }}%</td>
                  <td class="px-6 py-4 text-right font-mono text-slate-700">${{ ad.bid.toFixed(2) }}</td>
                  <td class="px-6 py-4 text-right font-mono font-semibold text-slate-900">${{ ad.cost.toFixed(2) }}</td>
                  <td
                    class="px-6 py-4 text-right font-mono font-semibold"
                    :class="ad.surplus >= 0 ? 'text-emerald-600' : 'text-rose-500'"
                  >
                    {{ ad.surplus >= 0 ? '+' : '' }}${{ ad.surplus.toFixed(2) }}
                  </td>
                </tr>
              </tbody>
              <tbody v-else class="divide-y divide-slate-100">
                <tr v-for="i in 4" :key="i" class="animate-pulse">
                  <td class="px-6 py-4">
                    <div class="h-3 w-24 rounded bg-slate-100"></div>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <div class="ml-auto h-3 w-14 rounded bg-slate-100"></div>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <div class="ml-auto h-3 w-12 rounded bg-slate-100"></div>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <div class="ml-auto h-3 w-12 rounded bg-slate-100"></div>
                  </td>
                  <td class="px-6 py-4 text-right">
                    <div class="ml-auto h-3 w-12 rounded bg-slate-100"></div>
                  </td>
                </tr>
              </tbody>
              </table>
            </div>
          </div>
        </section>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, defineAsyncComponent, onMounted, ref } from 'vue';
import axios from 'axios';
const MechanismChart = defineAsyncComponent(() => import('./components/MechanismChart.vue'));

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
const errorMessage = ref('');
const health = ref(null);
const healthError = ref('');
const lastLatencyMs = ref(null);
const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/$/, '');

const hasData = computed(() => results.value.length > 0);
const backendReady = computed(() => health.value?.status === 'ok');
const backendStatusLabel = computed(() => {
  if (healthError.value) return 'Backend unavailable';
  if (!health.value) return 'Backend unknown';
  return health.value.status === 'ok' ? 'Backend healthy' : 'Backend degraded';
});
const modelStatusLabel = computed(() => {
  if (!health.value) return 'unknown';
  return health.value.model_ready ? 'ready' : 'not_ready';
});
const latencyLabel = computed(() => {
  if (typeof lastLatencyMs.value !== 'number') return '--';
  return `${Math.round(lastLatencyMs.value)}ms`;
});

const summary = computed(() => {
  if (!results.value.length) {
    return {
      activeBidders: candidates.value.length,
      avgPctr: '0.00',
      totalCost: '0.00'
    };
  }
  const activeBidders = results.value.length;
  const avgPctrVal = results.value.reduce((s, r) => s + (r.pctr || 0), 0) / activeBidders;
  const totalCostVal = results.value.reduce((s, r) => s + (r.cost || 0), 0);
  return {
    activeBidders,
    avgPctr: (avgPctrVal * 100).toFixed(2),
    totalCost: totalCostVal.toFixed(2)
  };
});

const addCandidate = () => {
  candidates.value.push({ ad_id: `ad_${candidates.value.length + 1}`, bid: 1.0 });
};

const removeCandidate = (index) => {
  candidates.value.splice(index, 1);
};

const parseApiError = (error, fallback = 'Request failed') => {
  const detail = error?.response?.data?.detail;
  if (detail && typeof detail === 'object') {
    const code = detail.code ? `[${detail.code}] ` : '';
    const message = detail.message || fallback;
    return `${code}${message}`;
  }
  if (error?.message) {
    return error.message;
  }
  return fallback;
};

const fetchHealth = async () => {
  try {
    const response = await axios.get(`${apiBaseUrl}/healthz`);
    health.value = response.data;
    healthError.value = '';
  } catch (error) {
    healthError.value = parseApiError(error, 'Failed to load backend status');
  }
};

const runAuction = async () => {
  if (!userId.value.trim()) {
    errorMessage.value = 'User ID is required';
    return;
  }
  if (candidates.value.length === 0) {
    errorMessage.value = 'Please add at least one candidate';
    return;
  }
  const ids = new Set();
  for (const candidate of candidates.value) {
    if (!candidate.ad_id || !String(candidate.ad_id).trim()) {
      errorMessage.value = 'Each candidate must have a non-empty ad_id';
      return;
    }
    if (ids.has(candidate.ad_id.trim())) {
      errorMessage.value = `Duplicate ad_id: ${candidate.ad_id}`;
      return;
    }
    ids.add(candidate.ad_id.trim());
    if (!Number.isFinite(candidate.bid) || Number(candidate.bid) <= 0) {
      errorMessage.value = 'Each candidate must have bid > 0';
      return;
    }
  }

  errorMessage.value = '';
  loading.value = true;
  const started = performance.now();
  try {
    const response = await axios.post(`${apiBaseUrl}/recommend`, {
      user_id: userId.value.trim(),
      candidates: candidates.value.map((row) => ({
        ad_id: String(row.ad_id).trim(),
        bid: Number(row.bid)
      })),
      mechanism: mechanism.value
    });
    results.value = response.data.results;
    lastLatencyMs.value = performance.now() - started;
  } catch (error) {
    errorMessage.value = parseApiError(error, 'Failed to run auction');
  } finally {
    loading.value = false;
    await fetchHealth();
  }
};

onMounted(async () => {
  await fetchHealth();
});
</script>
