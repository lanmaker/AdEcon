<template>
  <div
    class="relative overflow-hidden rounded-xl border border-gray-100 bg-white p-5 shadow-[0_2px_8px_rgba(0,0,0,0.04)] transition hover:-translate-y-1 hover:shadow-[0_6px_16px_rgba(0,0,0,0.06)]"
    :class="{ 'ring-2 ring-indigo-200': isWinner }"
  >
    <div v-if="isWinner" class="absolute right-0 top-0 rounded-bl-lg bg-indigo-600 px-3 py-1 text-[11px] font-semibold uppercase tracking-wide text-white shadow-sm">
      Winner
    </div>

    <div class="mb-3 flex items-center justify-between">
      <h3 class="text-sm font-medium text-slate-700">Ad: {{ ad.ad_id }}</h3>
      <span class="text-xs font-semibold text-slate-400">Rank #{{ ad.rank }}</span>
    </div>

    <div class="flex items-baseline gap-2">
      <span class="text-2xl font-bold text-slate-900">${{ ad.cost.toFixed(2) }}</span>
      <span class="text-xs text-slate-500">CPC</span>
    </div>

    <div class="mt-4 space-y-2 border-t border-gray-100 pt-3 text-xs text-slate-600">
      <div class="flex justify-between">
        <span>Bid</span>
        <span class="font-semibold text-slate-800">${{ ad.bid.toFixed(2) }}</span>
      </div>
      <div class="flex justify-between">
        <span>pCTR</span>
        <span class="font-semibold text-emerald-600">{{ (ad.pctr * 100).toFixed(2) }}%</span>
      </div>
      <div class="flex justify-between">
        <span>Score (eCPM)</span>
        <span class="font-semibold text-slate-800">{{ ad.score.toFixed(4) }}</span>
      </div>
      <div class="flex justify-between">
        <span>Surplus</span>
        <span class="font-semibold text-indigo-600">${{ ad.surplus.toFixed(4) }}</span>
      </div>
    </div>

    <div class="mt-4 h-1.5 w-full overflow-hidden rounded-full bg-gray-100">
      <div
        class="h-full rounded-full bg-indigo-500"
        :style="{ width: Math.min(ad.pctr * 100, 100) + '%' }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { defineProps, computed } from 'vue';

const props = defineProps({
  ad: {
    type: Object,
    required: true
  }
});

const isWinner = computed(() => props.ad.rank === 1);
</script>
