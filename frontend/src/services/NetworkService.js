


export const getFractalJulia = async (body) => {
	return new Promise((resolve, reject) => {
		fetch("/api/julia", {
			method: "POST",
			body: JSON.stringify(body),
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