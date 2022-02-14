<template>
    <div class='content'>
        <el-card class='mb-2' shadow='hover'>
            <div class='py-4 font-bold'>工作台</div>
            <el-row>
                <el-col :xs='24' :md='16'>
                    <div class='flex items-center'>
                        <div class='pr-4 flex items-center'>
                            <el-avatar class='w-16 h-16' src='https://fuss10.elemecdn.com/e/5d/4a731a90594a4af544c0c25941171jpeg.jpeg' />
                        </div>
                        <div>
                            <div class='text-xl'>你好，{{ user.name }} ，祝你开心每一天！</div>
                            <div class='text-sm text-gray-400 pt-2'>账户长虹</div>
                        </div>
                    </div>
                </el-col>
                <!-- <el-col :xs='24' :md='8'>
                    <div class='flex items-center flex-row-reverse'>
                        <div class='px-1 text-center'>
                            <div class='text-sm text-gray-400 pb-2'>访问量</div>
                            <div class='text-xl'>3,344</div>
                        </div>
                        <el-divider direction='vertical' class='h-8' />
                        <div class='px-1 text-center'>
                            <div class='text-sm text-gray-400 pb-2'>排名</div>
                            <div class='text-xl'>1/100</div>
                        </div>
                        <el-divider direction='vertical' class='h-8' />
                        <div class='px-1 text-center'>
                            <div class='text-sm text-gray-400 pb-2'>项目数量</div>
                            <div class='text-xl'>100</div>
                        </div>
                    </div>
                </el-col> -->
            </el-row>
        </el-card>

        <el-row :gutter='15'>
            <el-col :md='24' :lg='24'>
                <List />
            </el-col>
            <!-- 
            <el-col :md='24' :lg='8'>
                <el-card shadow='hover' class='mb-2'>
                    <template #header>
                        <div class='card-header flex justify-between items-center'>
                            <span>快速开始</span>
                        </div>
                    </template>
                    <div class='flex flex-wrap'>
                        <div v-for='o in 7' :key='o' class='p-1'>
                            <el-tag>{{ '操作 ' + o }}</el-tag>
                        </div>
                    </div>
                </el-card>

                <Chart />
            </el-col> -->
        </el-row>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useLayoutStore } from '/@/store/modules/layout'
import Chart from '/@/views/Dashboard/Workplace/_Components/Chart.vue'
import List from '/@/views/Dashboard/Workplace/_Components/List.vue'

export default defineComponent({
    name: 'Workplace',
    components: {
        List,
        Chart
    },
    setup() {
        const { getUserInfo } = useLayoutStore()
        return {
            user: getUserInfo
        }
    }
})
</script>