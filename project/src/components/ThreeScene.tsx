import { useEffect, useRef } from 'react';
import * as THREE from 'three';

const ThreeScene = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const sceneRef = useRef<THREE.Scene | null>(null);
  const rendererRef = useRef<THREE.WebGLRenderer | null>(null);
  const particlesRef = useRef<THREE.Points | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight;

    const scene = new THREE.Scene();
    sceneRef.current = scene;
    scene.fog = new THREE.Fog(0x0a0e27, 100, 500);

    const camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 50;

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setClearColor(0x000000, 0.1);
    renderer.shadowMap.enabled = true;
    containerRef.current.appendChild(renderer.domElement);
    rendererRef.current = renderer;

    const particleGeometry = new THREE.BufferGeometry();
    const particleCount = 1500;
    const positions = new Float32Array(particleCount * 3);
    const velocities = new Float32Array(particleCount * 3);
    const sizes = new Float32Array(particleCount);

    for (let i = 0; i < particleCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 200;
      positions[i + 1] = (Math.random() - 0.5) * 200;
      positions[i + 2] = (Math.random() - 0.5) * 200;

      velocities[i] = (Math.random() - 0.5) * 0.2;
      velocities[i + 1] = (Math.random() - 0.5) * 0.2;
      velocities[i + 2] = (Math.random() - 0.5) * 0.2;

      sizes[i / 3] = Math.random() * 0.5 + 0.1;
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    particleGeometry.setAttribute('size', new THREE.BufferAttribute(sizes, 1));

    const particleMaterial = new THREE.PointsMaterial({
      color: 0x3b82f6,
      size: 0.3,
      transparent: true,
      opacity: 0.6,
      sizeAttenuation: true,
      fog: true,
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);
    particlesRef.current = particles;

    const shieldGeometry = new THREE.IcosahedronGeometry(15, 4);
    const shieldMaterial = new THREE.MeshStandardMaterial({
      color: 0x0ea5e9,
      wireframe: false,
      emissive: 0x0284c7,
      emissiveIntensity: 0.3,
      metalness: 0.7,
      roughness: 0.2,
      transparent: true,
      opacity: 0.8,
    });

    const shield = new THREE.Mesh(shieldGeometry, shieldMaterial);
    shield.position.z = 0;
    shield.castShadow = true;
    shield.receiveShadow = true;
    scene.add(shield);

    const shieldWireGeometry = new THREE.IcosahedronGeometry(15, 4);
    const wireframeMaterial = new THREE.MeshStandardMaterial({
      color: 0x06b6d4,
      wireframe: true,
      emissive: 0x0284c7,
      emissiveIntensity: 0.5,
      transparent: true,
      opacity: 0.3,
    });

    const wireframe = new THREE.Mesh(shieldWireGeometry, wireframeMaterial);
    wireframe.position.z = 0;
    wireframe.scale.set(1.1, 1.1, 1.1);
    scene.add(wireframe);

    const light1 = new THREE.PointLight(0x3b82f6, 2, 100);
    light1.position.set(30, 30, 30);
    light1.castShadow = true;
    scene.add(light1);

    const light2 = new THREE.PointLight(0x0284c7, 1.5, 100);
    light2.position.set(-30, -30, 30);
    scene.add(light2);

    const ambientLight = new THREE.AmbientLight(0x1e293b, 0.5);
    scene.add(ambientLight);

    let mouseX = 0;
    let mouseY = 0;

    const onMouseMove = (event: MouseEvent) => {
      mouseX = (event.clientX / width) * 2 - 1;
      mouseY = -(event.clientY / height) * 2 + 1;
    };

    window.addEventListener('mousemove', onMouseMove);

    const animate = () => {
      requestAnimationFrame(animate);

      shield.rotation.x += 0.001;
      shield.rotation.y += 0.002;
      shield.rotation.z += 0.0005;

      wireframe.rotation.x -= 0.0015;
      wireframe.rotation.y -= 0.001;

      shield.position.x = mouseX * 10;
      shield.position.y = mouseY * 10;

      if (particlesRef.current) {
        const positionAttribute = particleGeometry.getAttribute('position') as THREE.BufferAttribute;
        const positions = positionAttribute.array as Float32Array;

        for (let i = 0; i < positions.length; i += 3) {
          positions[i] += velocities[i];
          positions[i + 1] += velocities[i + 1];
          positions[i + 2] += velocities[i + 2];

          if (Math.abs(positions[i]) > 100) velocities[i] *= -1;
          if (Math.abs(positions[i + 1]) > 100) velocities[i + 1] *= -1;
          if (Math.abs(positions[i + 2]) > 100) velocities[i + 2] *= -1;
        }

        positionAttribute.needsUpdate = true;
      }

      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
      const newWidth = containerRef.current?.clientWidth || width;
      const newHeight = containerRef.current?.clientHeight || height;

      camera.aspect = newWidth / newHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('resize', handleResize);
      containerRef.current?.removeChild(renderer.domElement);
      renderer.dispose();
      particleGeometry.dispose();
      particleMaterial.dispose();
      shieldGeometry.dispose();
      shieldMaterial.dispose();
      shieldWireGeometry.dispose();
      wireframeMaterial.dispose();
    };
  }, []);

  return <div ref={containerRef} className="absolute inset-0 opacity-60" />;
};

export default ThreeScene;
