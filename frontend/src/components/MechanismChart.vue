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
    color: ['#f43f5e', '#3b82f6'], // Rose-500, Blue-500
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      backgroundColor: 'rgba(255, 255, 255, 0.9)',
      borderColor: '#e2e8f0',
      textStyle: {
        color: '#1e293b'
      }
    },
    legend: {
      data: ['Cost (CPC)', 'Surplus'],
      bottom: 0,
      textStyle: {
        color: '#64748b'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ads,
      axisLine: {
        lineStyle: {
          color: '#cbd5e1'
        }
      },
      axisLabel: {
        color: '#64748b'
      },
      axisTick: {
        show: false
      }
    },
    yAxis: {
      type: 'value',
      splitLine: {
        lineStyle: {
          color: '#f1f5f9',
          type: 'dashed'
        }
      },
      axisLabel: {
        color: '#64748b',
        formatter: '${value}'
      }
    },
    series: [
      {
        name: 'Cost (CPC)',
        type: 'bar',
        stack: 'total',
        barWidth: '40%',
        itemStyle: {
          borderRadius: [0, 0, 4, 4] // Bottom rounded
        },
        data: costs
      },
      {
        name: 'Surplus',
        type: 'bar',
        stack: 'total',
        itemStyle: {
          borderRadius: [4, 4, 0, 0] // Top rounded
        },
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
