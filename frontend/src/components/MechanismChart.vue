<template>
  <div ref="chartRef" style="width: 100%; height: 300px;"></div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
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
    
    // Handle resize
    window.addEventListener('resize', () => {
      chartInstance && chartInstance.resize();
    });
  }
};

const updateChart = () => {
  if (!chartInstance) return;

  const ads = props.results.map(r => r.ad_id);
  const costs = props.results.map(r => r.cost);
  const surplus = props.results.map(r => r.surplus);

  const option = {
    backgroundColor: 'transparent',
    textStyle: { color: '#cbd5e1' },
    color: [
      new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: '#38bdf8' },
        { offset: 1, color: '#6366f1' }
      ]),
      new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: '#a855f7' },
        { offset: 1, color: '#22d3ee' }
      ])
    ],
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
        shadowStyle: { color: 'rgba(59,130,246,0.08)' }
      },
      backgroundColor: 'rgba(15,23,42,0.9)',
      borderColor: '#334155',
      textStyle: { color: '#e2e8f0' }
    },
    legend: {
      data: ['Cost (CPC)', 'Surplus'],
      bottom: 0,
      textStyle: { color: '#94a3b8' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '12%',
      top: '6%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ads,
      axisLine: { lineStyle: { color: 'rgba(255,255,255,0.15)' } },
      axisLabel: { color: '#cbd5e1' },
      axisTick: { show: false }
    },
    yAxis: {
      type: 'value',
      splitLine: { lineStyle: { color: 'rgba(255,255,255,0.07)', type: 'dashed' } },
      axisLabel: { color: '#cbd5e1', formatter: '${value}' }
    },
    series: [
      {
        name: 'Cost (CPC)',
        type: 'bar',
        stack: 'total',
        barWidth: '40%',
        itemStyle: { borderRadius: [4, 4, 2, 2] },
        emphasis: { itemStyle: { shadowBlur: 12, shadowColor: 'rgba(56,189,248,0.35)' } },
        data: costs
      },
      {
        name: 'Surplus',
        type: 'bar',
        stack: 'total',
        itemStyle: { borderRadius: [10, 10, 4, 4] },
        emphasis: { itemStyle: { shadowBlur: 12, shadowColor: 'rgba(168,85,247,0.35)' } },
        data: surplus
      }
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
