<template>
  <el-card class="ad-card" :class="{ winner: isWinner }">
    <template #header>
      <div class="card-header">
        <span>Ad ID: {{ ad.ad_id }}</span>
        <el-tag v-if="isWinner" type="success">Winner</el-tag>
      </div>
    </template>
    <div class="card-body">
      <p><strong>Bid:</strong> ${{ ad.bid.toFixed(2) }}</p>
      <p><strong>pCTR:</strong> {{ (ad.pctr * 100).toFixed(4) }}%</p>
      <p><strong>Score (eCPM):</strong> {{ ad.score.toFixed(4) }}</p>
      <el-divider />
      <p><strong>Rank:</strong> {{ ad.rank }}</p>
      <p><strong>Cost (CPC):</strong> <span class="cost">${{ ad.cost.toFixed(4) }}</span></p>
      <p><strong>Surplus:</strong> <span class="surplus">${{ ad.surplus.toFixed(4) }}</span></p>
    </div>
  </el-card>
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

<style scoped>
.ad-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}
.ad-card.winner {
  border: 2px solid #67c23a;
  transform: scale(1.02);
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.cost {
  color: #f56c6c;
  font-weight: bold;
}
.surplus {
  color: #409eff;
  font-weight: bold;
}
</style>
