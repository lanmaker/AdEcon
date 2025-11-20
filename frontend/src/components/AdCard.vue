<template>
  <div
    class="relative overflow-hidden rounded-2xl border border-white/10 bg-white/5 p-5 shadow-xl backdrop-blur-lg transition-all hover:-translate-y-1 hover:bg-white/10"
    :class="{ 'ring-2 ring-emerald-400/60 ring-offset-2 ring-offset-black/40': isWinner }"
  >
    <div v-if="isWinner" class="absolute right-0 top-0 rounded-bl-xl bg-emerald-500 px-3 py-1 text-[11px] font-bold uppercase tracking-wide text-white shadow-lg shadow-emerald-500/30">
      Winner
    </div>

    <div class="mb-3 flex items-center justify-between">
      <h3 class="text-sm font-medium text-slate-200">Ad: {{ ad.ad_id }}</h3>
      <span class="text-xs font-semibold text-slate-400">Rank #{{ ad.rank }}</span>
    </div>

    <div class="flex items-baseline gap-2">
      <span class="text-3xl font-bold text-slate-50">${{ ad.cost.toFixed(2) }}</span>
      <span class="text-xs text-slate-500">CPC</span>
    </div>

    <div class="mt-4 space-y-2 border-t border-white/10 pt-3 text-xs text-slate-300">
      <div class="flex justify-between">
        <span>Bid</span>
        <span class="font-semibold text-slate-100">${{ ad.bid.toFixed(2) }}</span>
      </div>
      <div class="flex justify-between">
        <span>pCTR</span>
        <span class="font-semibold text-emerald-300">{{ (ad.pctr * 100).toFixed(2) }}%</span>
      </div>
      <div class="flex justify-between">
        <span>Score (eCPM)</span>
        <span class="font-semibold text-slate-100">{{ ad.score.toFixed(4) }}</span>
      </div>
      <div class="flex justify-between">
        <span>Surplus</span>
        <span class="font-semibold text-cyan-300">${{ ad.surplus.toFixed(4) }}</span>
      </div>
    </div>

    <div class="mt-4 h-1.5 w-full overflow-hidden rounded-full bg-white/10">
      <div
        class="h-full rounded-full bg-gradient-to-r from-blue-500 via-indigo-500 to-purple-500"
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
