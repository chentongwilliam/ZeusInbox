<template>
  <div class="w-full h-full flex flex-col">
    <!-- 顶部导航栏 -->
    <div class="flex items-center justify-between mb-6">
      <div class="flex gap-2">
        <button class="px-4 py-2 rounded-t-lg bg-white border-b-2 border-green-500 font-semibold text-gray-900 shadow-none">Rules</button>
        <button class="px-4 py-2 rounded-t-lg bg-gray-100 text-gray-500 shadow-none">Pending</button>
        <button class="px-4 py-2 rounded-t-lg bg-gray-100 text-gray-500 shadow-none">History</button>
        <button class="px-4 py-2 rounded-t-lg bg-gray-100 text-gray-500 shadow-none">Test</button>
        <button class="px-4 py-2 rounded-t-lg bg-gray-100 text-gray-500 shadow-none">Groups</button>
      </div>
      <div class="flex gap-2">
        <button class="px-4 py-2 bg-gray-100 text-gray-700 rounded-md border border-gray-200 font-medium">Bulk Run on Inbox</button>
        <button class="px-4 py-2 bg-gray-900 text-white rounded-md font-semibold shadow">Create Automation</button>
      </div>
    </div>
    <!-- 表格 -->
    <div class="bg-white rounded-xl shadow border overflow-x-auto flex-1">
      <table class="min-w-full text-left">
        <thead class="bg-gray-50 text-gray-500 text-sm">
          <tr>
            <th class="px-6 py-3 font-medium">Name</th>
            <th class="px-6 py-3 font-medium">Conditions</th>
            <th class="px-6 py-3 font-medium">Type</th>
            <th class="px-6 py-3 font-medium">Actions</th>
            <th class="px-6 py-3 font-medium">Automated</th>
            <th class="px-6 py-3 font-medium">Threads</th>
            <th class="px-6 py-3 font-medium"></th>
          </tr>
        </thead>
        <tbody>
          <!-- 空表格，无数据 -->
          <tr>
            <td colspan="7" class="text-center text-gray-400 py-12">No automations yet.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template> 