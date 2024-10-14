


export const getFractal = async (params) => {
	return new Promise((resolve, reject) => {
		fetch(`/api/render/image/${params?.type ?? "julia"}`, {
			method: "POST",
			body: JSON.stringify(params),
			headers: {
				"Content-Type": "application/json",
			},
		})
		.then((res) => res.json())
		.then((user) => {
			resolve(user);
		})
		.catch((e) => reject(`failed to get julia fractal: ${e}`));
	});
};