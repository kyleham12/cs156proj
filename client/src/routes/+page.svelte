<script lang="ts">
	import { onMount } from 'svelte';
	
	let showRec: boolean = false;
	let recList: any[] = [];
	let selected_song: string = "";
	let checkboxValues: any[] = [[false, false], [false, false], [false, false], [false, false], [false, false],
								 [false, false], [false, false], [false, false], [false, false], [false, false]];
	let songSelect:any[] = [];
	let searchType = "Song";
	let searchString = "";
	let searchArray: any[] = [];
	let search = false;
	let selected_artist = "";
	let savingOpinion = false;

	async function getSongsList() { 
		try {
			const response = await fetch('/getSongsList');
			const data = await response.json();
			let songList = data.songList;
			let artist_list = data.artist_list;
			let image_list = data.image_list;
			songSelect = [];
			for(let i = 0; i < songList.length; i++) {
				songSelect.push([songList[i], artist_list[i], image_list[i]]);
			}
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
			selected_song = "";
			checkboxValues = [[false, false], [false, false], [false, false], [false, false], [false, false],
							  [false, false], [false, false], [false, false], [false, false], [false, false]];
			searchString = "";
			searchArray = [];
			selected_artist = "";
			savingOpinion = false;
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
		savingOpinion = true;
		returnOpinion();
	}

	function getSearchResult() {
		searchArray = [];
		if (searchType == "Song") {
			for(let i = 0; i < songSelect.length; i++) {
				if (songSelect[i][0].toLowerCase().includes(searchString.toLowerCase())) {
					searchArray.push(songSelect[i]);
				}
			}
			searchArray = searchArray.sort((a: any, b: any) => a[0].localeCompare(b[0]));
		} else {
			for(let i = 0; i < songSelect.length; i++) {
				if (songSelect[i][1].toLowerCase().includes(searchString.toLowerCase())) {
					searchArray.push(songSelect[i]);
				}
			}
			searchArray = searchArray.sort((a: any, b: any) => a[1].localeCompare(b[1]));
		}
		search = true;
	}

	function handleItemClick(item: any) {
		selected_song = item[0];
		selected_artist = item[1];
		search = false;
		showRecButton();
	}
</script>

<svelte:head>
	<title>Music Recommender</title>
	<meta name="description" content="Home page" />
</svelte:head>
<html lang="ts">
	<div class="join w-full pt-8 pb-10">
		<select class="select select-bordered join-item rounded-l-full" bind:value={searchType}>
			<option selected>Song</option>
			<option>Artist</option>
		</select>
		<div class="card join-item w-full">
			<input type="text" placeholder="Search for {searchType}" bind:value={searchString} class="input input-bordered w-full rounded-none" />
		</div>
		<button class="btn btn-outline join-item rounded-r-full" on:click={getSearchResult}>Search</button>
	</div>
	{#if search}
		{#if searchArray.length > 0}
			<div class="display-body overflow-x-auto">
				<div class="grid-container">
					{#each searchArray as searchItem, index}
						{#if searchItem}
							<!-- svelte-ignore a11y-no-static-element-interactions -->
							<!-- svelte-ignore a11y-click-events-have-key-events -->
							<div class="card card-compact options shadow-lg" on:click={() => handleItemClick(searchItem)}>
								<div class="card-body">
									<h2 class="card-title text-lg">{searchItem[0]}</h2>
									<p class="text-md">{searchItem[1]}</p>
								</div>
							</div>
						{/if}
					{/each}
				</div>
			</div>
		{:else}
			<h2 class="pl-2">No match found</h2>
		{/if}
	{:else}
		{#if showRec}
			<h2 class="pt-4">Selected Song: {selected_song} by {selected_artist}</h2>

			<h2 class="pt-6">Recommended Songs</h2>
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
									{#if savingOpinion}
										<td><input type="checkbox" class="checkbox" disabled bind:checked={checkboxValues[rowIndex][0]}/></td>
										<td><input type="checkbox" class="checkbox" disabled bind:checked={checkboxValues[rowIndex][1]}/></td>
									{:else}
										<td><input type="checkbox" class="checkbox" bind:checked={checkboxValues[rowIndex][0]} on:change={() => toggleCheckbox(rowIndex, 0)}/></td>
										<td><input type="checkbox" class="checkbox" bind:checked={checkboxValues[rowIndex][1]} on:change={() => toggleCheckbox(rowIndex, 1)}/></td>
									{/if}
								</tr>
							{/if}
						{/each}
						{#if recList.length > 0}
							<tr>
								<td colspan="4">
									{#if savingOpinion}
										<button class="btn btn-outline btn-disabled w-full">Processing Opinion, Please Wait</button>
									{:else}
										<button class="btn btn-outline w-full" on:click={submitOpinion}>Submit Opinion</button>
									{/if}
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
	{/if}
</html>

<style>
	@import 'tailwindcss/base';
	@import 'tailwindcss/components';
	@import 'tailwindcss/utilities';

	select,option,input, h2, div, tr, th {
		font-family: 'BadComic';
	}

	.grid-container {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(275px, 1fr)); /* Use minmax for flexible column sizing */
		gap: 20px; /* Adjust the gap between items */
		justify-content: center; /* Center items within the grid */
	}

	.display-body {
		margin: 0;
		padding: 10px;
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	.options {
		width: 275px;
	}

	.options:hover {
		transform: scale(1.05); /* Increase the size of the card on hover */
	}
</style>
