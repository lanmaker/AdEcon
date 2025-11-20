<template>
  <div 
    class="relative overflow-hidden rounded-xl border border-slate-200 bg-white p-5 shadow-sm transition-all hover:-translate-y-1 hover:shadow-md"
    :class="{ 'ring-2 ring-green-500 ring-offset-2': isWinner }"
  >
    <div v-if="isWinner" class="absolute right-0 top-0 rounded-bl-lg bg-green-600 px-3 py-1 text-xs font-bold text-white shadow-sm">
      WINNER
    </div>
    
    <div class="mb-3 flex items-center justify-between">
      <h3 class="text-sm font-medium text-slate-500">Ad ID: {{ ad.ad_id }}</h3>
      <span class="text-xs font-semibold text-slate-400">Rank #{{ ad.rank }}</span>
    </div>

    <div class="flex items-baseline gap-2">
      <span class="text-2xl font-bold text-slate-900">${{ ad.cost.toFixed(2) }}</span>
      <span class="text-xs text-slate-400">CPC</span>
    </div>

    <div class="mt-4 space-y-2 border-t border-slate-100 pt-3 text-xs">
      <div class="flex justify-between">
        <span class="text-slate-500">Bid</span>
        <span class="font-medium text-slate-700">${{ ad.bid.toFixed(2) }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-slate-500">pCTR</span>
        <span class="font-medium text-emerald-600">{{ (ad.pctr * 100).toFixed(2) }}%</span>
      </div>
      <div class="flex justify-between">
        <span class="text-slate-500">Score (eCPM)</span>
        <span class="font-medium text-slate-700">{{ ad.score.toFixed(4) }}</span>
      </div>
      <div class="flex justify-between">
        <span class="text-slate-500">Surplus</span>
        <span class="font-medium text-blue-600">${{ ad.surplus.toFixed(4) }}</span>
      </div>
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
