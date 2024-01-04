<template lang="">
    <div class="max-w-7xl mx-auto grid grid-cols-4 gap-4">
        <div class="main-left col-span-1">
            <div class="bg-white border border-gray-200 rounded-lg text-center p-4">
                <div class="space-y-4">
                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">

                            <p class="text-xs"><strong>Sarah</strong></p>
                        </div>

                        <span class="text-xs text-gray-500">18 minutes ago</span>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">

                            <p class="text-xs"><strong>Mary</strong></p>
                        </div>

                        <span class="text-xs text-gray-500">18 minutes ago</span>
                    </div>

                    <div class="flex items-center justify-between">
                        <div class="flex items-center space-x-2">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">

                            <p class="text-xs"><strong>John</strong></p>
                        </div>

                        <span class="text-xs text-gray-500">18 minutes ago</span>
                    </div>
                </div>
            </div>

        </div>
        <div class="main-center col-span-3 space-y-4 ">
            <div class="bg-white border border-gray-200 rounded-lg ">
                <div class="flex flex-col flex-grow p-4 h-[calc(100vh-339px)] overflow-auto">
                    <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                        <div>
                            <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                                    eiusmod.</p>
                            </div>
                            <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                        </div>
                        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                        </div>
                    </div>
                    <div class="flex w-full mt-2 space-x-3 max-w-md ml-auto justify-end">
                        <div>
                            <div class="bg-blue-600 text-white p-3 rounded-l-lg rounded-br-lg">
                                <p class="text-sm">Lorem ipsum dolor sit amet asfsaf.</p>
                            </div>
                            <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                        </div>
                        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                        </div>
                    </div>
                    <div class="flex w-full mt-2 space-x-3 max-w-md">
                        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                        </div>
                        <div>
                            <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                                    eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                            </div>
                            <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                        </div>
                    </div>
                    <div class="flex w-full mt-2 space-x-3 max-w-md">
                        <div class="flex-shrink-0 h-10 w-10 rounded-full bg-gray-300">
                            <img src="https://i.pravatar.cc/300?img=70" class="w-[40px] rounded-full">
                        </div>
                        <div>
                            <div class="bg-gray-300 p-3 rounded-r-lg rounded-bl-lg">
                                <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                                    eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                            </div>
                            <span class="text-xs text-gray-500 leading-none">2 min ago</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="bg-white border border-gray-200 rounded-lg">
                <div class="p-4">
                    <textarea class="w-full bg-gray-100 rounded-lg p-4 resize-none"
                        placeholder="What do you want to say?" rows="" cols=""></textarea>
                </div>
                <div class="mb-2 border-t border-gray-100 p-4 flex justify-between">
                    <a href="#" class="inline-block py-4 px-6 bg-purple-600 text-white rounded-lg">Send</a>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {}
</script>
