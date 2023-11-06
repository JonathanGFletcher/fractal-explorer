export const signUp = async (username, password) => {
	return new Promise((resolve, reject) => {
		fetch("/api/signup", {
			method: "POST",
			body: JSON.stringify({ username, password }),
			headers: {
				"Content-Type": "application/json",
			},
		})
			.then((res) => res.json())
			.then((user) => {
				resolve(user);
			})
			.catch((e) => reject(`Failed to sign up: ${e}`));
	});
};

export const signIn = async (username, password) => {
	return new Promise((resolve, reject) => {
		fetch("/api/signin", {
			method: "POST",
			body: JSON.stringify({ username, password }),
			headers: {
				"Content-Type": "application/json",
			},
		})
			.then((res) => res.json())
			.then((user) => {
				resolve(user);
			})
			.catch((e) => reject(`Failed to sign in: ${e}`));
	});
};

export const fetchSystemInfo = async (systemName = "mothership") => {
	return new Promise((resolve, reject) => {
		fetch(`/api/system-info?name=${systemName}`)
			.then((res) => res.json())
			.then((json) => {
				const payloadStr = json?.payload;
				if (payloadStr === null) throw "Failed to get payload";

				const payload = JSON.parse(payloadStr);
				resolve(payload);
			})
			.catch((e) => reject(`Failed to fetch system info: ${e}`));
	});
};

export const fetchFileObjects = async () => {
	try {
		const res = await fetch(`/api/file-objects`);
		const data = await res.json();
		return data;
	} catch (e) {
		throw e;
	}
};

export const fetchFileObjectStatus = async () => {
	try {
		const res = await fetch(`/api/file-objects/storage/config`, {
			method: "POST",
			body: JSON.stringify({ keys: [] }),
		});
		const data = await res.json();
		return data;
	} catch (e) {
		throw e;
	}
};

export const fetchJobs = async () => {
	try {
		const res = await fetch(`/api/queue/sync/jobs`);
		const data = await res.json();
		return data;
	} catch (e) {
		throw e;
	}
}