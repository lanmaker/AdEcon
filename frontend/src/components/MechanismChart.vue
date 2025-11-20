<template>
  <div ref="chartRef" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  results: {
    type: Array,
    required: true
  }
});

const chartRef = ref(null);
let chartInstance = null;

const initChart = () => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    updateChart();
  }
};

const updateChart = () => {
  if (!chartInstance) return;

  const ads = props.results.map(r => r.ad_id);
  const bids = props.results.map(r => r.bid);
  const costs = props.results.map(r => r.cost);
  const surplus = props.results.map(r => r.surplus);

  const option = {
    title: {
      text: 'Auction Dynamics (Bid vs Cost vs Surplus)'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['Cost', 'Surplus']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ads
    },
    yAxis: {
      type: 'value',
      name: 'Price ($)'
    },
    series: [
      {
        name: 'Cost',
        type: 'bar',
        stack: 'total',
        emphasis: {
          focus: 'series'
        },
        data: costs,
        itemStyle: {
          color: '#f56c6c'
        }
      },
      {
        name: 'Surplus',
        type: 'bar',
        stack: 'total',
        emphasis: {
          focus: 'series'
        },
        data: surplus,
        itemStyle: {
          color: '#409eff'
        }
      }
      // Note: Bid is Cost + Surplus, so stacking them equals Bid (roughly, if we ignore rationality clamp)
    ]
  };

  chartInstance.setOption(option);
};

onMounted(() => {
  initChart();
});

watch(() => props.results, () => {
  updateChart();
}, { deep: true });
</script>
