Module.onRuntimeInitialized = () => {
    const width = 300;
    const height = 200;
    let bitmap = new Float32Array(width * height * 3);
    let colorsteps = [
        { value: 0.0 , rgb: {x: 17/255, y: 3/255, z: 77/255} },
        { value: 0.03 , rgb: {x: 38/255, y: 15/255, z: 141/255} },
        { value: 0.05 , rgb: {x: 111/255, y: 45/255, z: 12/255} },
        { value: 0.25 , rgb: {x: 203/255, y: 52/255, z: 82/255} },
        { value: 0.5 , rgb: {x: 250/255, y: 102/255, z: 34/255} },
        { value: 0.85 , rgb: {x: 254/255, y: 221/255, z: 8/255} },
        { value: 0.95 , rgb: {x: 101/255, y: 240/255, z: 142/255} },
        { value: 1.0 , rgb: {x: 255/255, y: 255/255, z: 255/255} }
    ]
    const constant = { x: -0.7365, y: 0.156 };
    const maxIterations = 500;
    const scale = 1.0;
    const samples = 1;
    const center = { x: 0.0, y: 0.0 };

    const renderJuliaDouble = Module.cwrap(
        "render_julia_double",
        "void",
        ["number", "number", "number", "number", "number", "number", "number", "number", "number", "number", "number"]
    );

    console.log("Rendering...");
    // let result = renderJuliaDouble(
    //     bitmap.byteOffset,
    //     1,
    //     width,
    //     height,
    //     colorsteps,
    //     colorsteps.length,
    //     constant,
    //     maxIterations,
    //     scale,
    //     samples,
    //     center
    // );

    // console.log(result);
}
