<script lang="ts">
	import { onMount } from 'svelte';

	
	let showRec: boolean = false;
	let songList: any[] = [];
	let recList: any[] = [];
	let selected_song: string = "";
	let checkboxValues: any[] = [[false, false], [false, false], [false, false], [false, false], [false, false],
								 [false, false], [false, false], [false, false], [false, false], [false, false]];


	async function getSongsList() { 
		try {
			const response = await fetch('/getSongsList');
			const data = await response.json();
			songList = data.songList;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	async function getRecList() {
		try {
			const response = await fetch('/getRecList', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({selected_song: selected_song})
			});
			const data = await response.json();
			recList = data.recList;
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}

	onMount(() => {
		getSongsList();
	});

	function toggleCheckbox(rowIndex: number, colIndex: number) {
		if (colIndex == 0) {
			if((checkboxValues[rowIndex][colIndex]) && checkboxValues[rowIndex][colIndex + 1]) {
				checkboxValues[rowIndex][colIndex + 1] = false;
			}
		} else {
			if((checkboxValues[rowIndex][colIndex]) && checkboxValues[rowIndex][colIndex - 1]) {
				checkboxValues[rowIndex][colIndex - 1] = false;
			}
		}
	}

	function showRecButton() {
		if (selected_song != "") {
			getRecList();
			showRec = true;
		}
    }

	function submitOpinion() {
		returnOpinion();
	}

	async function returnOpinion() {
		let returnInfo: any[] = [];
		for(let i = 0; i < checkboxValues.length; i++) {
			if (checkboxValues[i][0] | checkboxValues[i][1]) {
				let temp: any[] = [recList[i][0],recList[i][1], 0];
				if (checkboxValues[i][0]) {
					temp[2] = 1;
				} else {
					temp[2] = -1;
				}
				returnInfo.push(temp);
			}
		}
		console.log(returnInfo);

		try {
			const response = await fetch('/getOpinion', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({selected_song: selected_song, returnInfo: returnInfo})
			});
			const data = await response.json();
			console.log(data.msg);

			showRec = false;
			recList = [];
			selected_song = ""
			console.log(checkboxValues);
			checkboxValues = [[false, false], [false, false], [false, false], [false, false], [false, false],
							  [false, false], [false, false], [false, false], [false, false], [false, false]];
		} catch (error) {
			console.error('Error fetching data:', error);
		}
	}
</script>

<svelte:head>
	<title>Music Recommender</title>
	<meta name="description" content="Home page" />
</svelte:head>
<html lang="ts">
	<h2 class="pb-2 pt-4">Selected Song</h2>
	<div class="join w-full">
		<select class="select select-bordered join-item w-full" bind:value={selected_song}>
			{#each songList as song, rowIndex}
				<option>{song}</option>
			{/each}
		</select>
		<button class="btn btn-outline join-item rounded-r-full" on:click={showRecButton}>Show Recommendations</button>
	</div>

	{#if showRec}
		<h2 class="pt-10">Recommended Songs</h2>
		<div class="overflow-x-auto">
			<table class="table">
				<thead>
					<tr>
						<th>Song</th>
						<th class="pr-10"></th>
						<th>Like</th>
						<th>Dislike</th>
					</tr>
				</thead>
				<tbody>
					{#each recList as recSong, rowIndex}
						{#if recSong}
							<tr>
								<td>
									<div class="flex items-center gap-3">
										<div class="avatar">
											<div class="mask mask-squircle w-14 h-14">
												<img src={recSong[2]} alt="Avatar Tailwind CSS Component" />
											</div>
										</div>
										<div>
											<div class="font-bold">{recSong[0]}</div>
											<div class="text-sm opacity-50">{recSong[1]}</div>
										</div>
									</div>
								</td>
								<td></td>
								<td><input type="checkbox" class="checkbox" bind:checked={checkboxValues[rowIndex][0]} on:change={() => toggleCheckbox(rowIndex, 0)}/></td>
								<td><input type="checkbox" class="checkbox" bind:checked={checkboxValues[rowIndex][1]} on:change={() => toggleCheckbox(rowIndex, 1)}/></td>
							</tr>
						{/if}
					{/each}
					{#if recList.length > 0}
						<tr>
							<td colspan="4">
								<button class="btn btn-outline w-full" on:click={submitOpinion}>Submit Opinion</button>
							</td>
						</tr>
					{:else}
						<tr>
							<td>
								<div class="flex items-center gap-3">
									<div class="avatar">
										<div class="mask mask-squircle w-14 h-14">
											<div class="skeleton w-14 h-14"></div>
										</div>
									</div>
									<div class="flex flex-col gap-4 w-full">
										<div class="skeleton h-3 w-full"></div>
										<div class="skeleton h-3 w-30"></div>
									</div>
								</div>
							</td>
							<td></td>
							<td><div class="skeleton w-6 h-6"></div></td>
							<td><div class="skeleton w-6 h-6"></div></td>
						</tr>
					{/if}
				</tbody>
			</table>
		</div>
	{/if}
</html>

<style>
	@import 'tailwindcss/base';
	@import 'tailwindcss/components';
	@import 'tailwindcss/utilities';

	select,option,input, h2, div, tr, th {
		font-family: 'BadComic';
	}
</style>
