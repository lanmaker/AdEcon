<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <h1>AdEcon: Real-time Advertising Auction</h1>
      </el-header>
      <el-main>
        <el-row :gutter="20">
          <!-- Configuration Panel -->
          <el-col :span="6">
            <el-card>
              <template #header>
                <div class="card-header">
                  <span>Configuration</span>
                </div>
              </template>
              <el-form label-position="top">
                <el-form-item label="User ID">
                  <el-input v-model="userId" placeholder="dev_412" />
                </el-form-item>
                <el-form-item label="Mechanism">
                  <el-radio-group v-model="mechanism">
                    <el-radio-button label="gsp">GSP</el-radio-button>
                    <el-radio-button label="vcg">VCG</el-radio-button>
                  </el-radio-group>
                </el-form-item>
                <el-divider>Candidates</el-divider>
                <div v-for="(cand, index) in candidates" :key="index" class="candidate-row">
                  <el-input v-model="cand.ad_id" placeholder="Ad ID" style="width: 100px; margin-right: 5px;" />
                  <el-input-number v-model="cand.bid" :min="0" :step="0.1" style="width: 120px;" />
                  <el-button type="danger" icon="Delete" circle size="small" @click="removeCandidate(index)" style="margin-left: 5px;" />
                </div>
                <el-button type="primary" plain style="width: 100%; margin-top: 10px;" @click="addCandidate">Add Candidate</el-button>
                
                <el-divider />
                <el-button type="success" style="width: 100%;" @click="runAuction" :loading="loading">Run Auction</el-button>
              </el-form>
            </el-card>
          </el-col>
          
          <!-- Results Panel -->
          <el-col :span="18">
            <div v-if="results.length > 0">
              <el-row :gutter="20">
                <el-col :span="24">
                  <el-card class="box-card">
                    <MechanismChart :results="results" />
                  </el-card>
                </el-col>
              </el-row>
              <el-divider />
              <el-row :gutter="20">
                <el-col :span="8" v-for="res in results" :key="res.ad_id">
                  <AdCard :ad="res" />
                </el-col>
              </el-row>
            </div>
            <el-empty v-else description="Run auction to see results" />
          </el-col>
        </el-row>
      </el-main>
    </el-container>
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

<style>
.common-layout {
  padding: 20px;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}
h1 {
  text-align: center;
  color: #303133;
}
.candidate-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}
</style>
