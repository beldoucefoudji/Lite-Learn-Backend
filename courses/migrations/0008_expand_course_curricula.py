from django.db import migrations


CURRICULA = {
    'mastering-typescript': {
        'video_url': 'https://www.youtube.com/embed/30LWjhZzg50',
        'lessons': [
            (
                'Introduction to TypeScript',
                'Understand why TypeScript exists, how it improves JavaScript development, and how to configure a TypeScript project.\n\nCore concepts:\n- Static typing and type inference\n- Installing TypeScript and configuring tsconfig.json\n- Compiling TypeScript to JavaScript\n- Reading and fixing compiler errors',
            ),
            (
                'Types, Interfaces, and Type Aliases',
                'Model application data with primitive types, unions, intersections, interfaces, and reusable type aliases.\n\nCore concepts:\n- Primitive and literal types\n- Optional and readonly properties\n- Interface extension\n- Union and intersection types',
            ),
            (
                'Functions and Generics',
                'Build reusable, type-safe functions and components that preserve information across inputs and outputs.\n\nCore concepts:\n- Parameter and return types\n- Function overloads\n- Generic constraints\n- keyof and indexed access types',
            ),
            (
                'Classes and Advanced Types',
                'Apply object-oriented patterns and TypeScript utility types to organize larger applications.\n\nCore concepts:\n- Access modifiers and abstract classes\n- Type guards and narrowing\n- Mapped and conditional types\n- Partial, Pick, Omit, and Record',
            ),
            (
                'Building a Type-Safe Application',
                'Combine the course concepts in a practical application with typed API responses, error handling, and maintainable project structure.\n\nCore concepts:\n- Typing asynchronous code\n- Safe API data handling\n- Module organization\n- Testing type contracts',
            ),
        ],
    },
    'ux-design-fundamentals': {
        'video_url': 'https://www.youtube.com/embed/c9Wg6Cb_YlU',
        'lessons': [
            (
                'Introduction to UX Design',
                'Learn how user experience design connects user needs, business goals, and accessible digital interfaces.\n\nCore concepts:\n- UX and UI responsibilities\n- Human-centered design\n- Design thinking process\n- Accessibility foundations',
            ),
            (
                'User Research and Personas',
                'Turn interviews and observations into useful insights, personas, and clearly framed user problems.\n\nCore concepts:\n- Research goals and interview plans\n- Qualitative and quantitative evidence\n- Personas and empathy maps\n- Problem statements',
            ),
            (
                'Information Architecture and User Flows',
                'Organize content and map the steps users take to complete important tasks.\n\nCore concepts:\n- Content hierarchy\n- Card sorting and navigation\n- Task flows and journey maps\n- Reducing cognitive load',
            ),
            (
                'Wireframes and Prototypes',
                'Move from rough ideas to testable interactive prototypes using layout and interaction principles.\n\nCore concepts:\n- Low and high-fidelity wireframes\n- Responsive layout systems\n- Interaction states\n- Prototype testing',
            ),
            (
                'Usability Testing and Iteration',
                'Plan usability sessions, recognize patterns in feedback, and improve a design using evidence.\n\nCore concepts:\n- Test scripts and success criteria\n- Observing without leading\n- Prioritizing usability findings\n- Iterative design decisions',
            ),
        ],
    },
    'data-systems-at-scale': {
        'video_url': 'https://www.youtube.com/embed/cQP8WApzIQQ',
        'lessons': [
            (
                'Introduction to Distributed Systems',
                'Explore why large systems distribute work across machines and the tradeoffs this introduces.\n\nCore concepts:\n- Scalability and fault tolerance\n- Network boundaries\n- Partial failures\n- Latency and throughput',
            ),
            (
                'Replication and Consistency',
                'Understand how replicated data remains available and how consistency models affect application behavior.\n\nCore concepts:\n- Leader and follower replication\n- Quorum reads and writes\n- Strong and eventual consistency\n- Conflict resolution',
            ),
            (
                'Partitioning and Database Sharding',
                'Distribute large datasets while avoiding hotspots and maintaining efficient queries.\n\nCore concepts:\n- Horizontal partitioning\n- Hash and range sharding\n- Rebalancing data\n- Cross-shard operations',
            ),
            (
                'Messaging and Event-Driven Architecture',
                'Design reliable asynchronous workflows using queues, event streams, and idempotent consumers.\n\nCore concepts:\n- Message brokers and logs\n- Delivery guarantees\n- Idempotency\n- Eventual consistency workflows',
            ),
            (
                'Reliability and Observability',
                'Operate distributed services with meaningful metrics, tracing, recovery strategies, and capacity planning.\n\nCore concepts:\n- Service-level objectives\n- Logs, metrics, and traces\n- Circuit breakers and retries\n- Disaster recovery',
            ),
        ],
    },
    'product-strategy-101': {
        'video_url': 'https://www.youtube.com/embed/yUOC-Y0f5ZQ',
        'lessons': [
            (
                'Introduction to Product Strategy',
                'Connect customer problems and company goals to a focused product direction.\n\nCore concepts:\n- Product vision and mission\n- Customer value\n- Strategic choices\n- Outcomes versus outputs',
            ),
            (
                'Market and Customer Discovery',
                'Evaluate market opportunities and discover high-value customer problems before committing to solutions.\n\nCore concepts:\n- Market segmentation\n- Jobs to be done\n- Competitor analysis\n- Opportunity sizing',
            ),
            (
                'Prioritization and Roadmaps',
                'Create a roadmap that communicates intent while remaining adaptable as evidence changes.\n\nCore concepts:\n- Impact and effort analysis\n- RICE and other prioritization methods\n- Now-next-later roadmaps\n- Managing dependencies',
            ),
            (
                'Metrics and Experimentation',
                'Define success measures and use experiments to reduce uncertainty before scaling an idea.\n\nCore concepts:\n- North-star and supporting metrics\n- Leading and lagging indicators\n- Hypothesis design\n- Experiment interpretation',
            ),
            (
                'Stakeholder Alignment',
                'Communicate tradeoffs, build shared context, and keep delivery teams aligned around product outcomes.\n\nCore concepts:\n- Strategy narratives\n- Decision records\n- Stakeholder mapping\n- Product reviews',
            ),
        ],
    },
    'rust-for-webassembly': {
        'video_url': 'https://www.youtube.com/embed/hcA_GuZHyZM',
        'lessons': [
            (
                'Introduction to Rust and WebAssembly',
                'Understand where WebAssembly fits on the web and how Rust produces compact, high-performance modules.\n\nCore concepts:\n- WebAssembly runtime model\n- Rust toolchain setup\n- wasm-pack and project structure\n- JavaScript interoperability',
            ),
            (
                'Rust Ownership and Memory Safety',
                'Use ownership, borrowing, and lifetimes to write safe code without a garbage collector.\n\nCore concepts:\n- Ownership rules\n- References and borrowing\n- Lifetimes\n- Result and Option',
            ),
            (
                'Building a WebAssembly Module',
                'Compile Rust functions into a browser-ready module and expose a clean JavaScript interface.\n\nCore concepts:\n- wasm-bindgen\n- Exporting Rust functions\n- Passing strings and arrays\n- Build targets',
            ),
            (
                'Browser and DOM Integration',
                'Connect WebAssembly logic to browser APIs while keeping rendering and computation responsibilities clear.\n\nCore concepts:\n- web-sys and js-sys\n- DOM events\n- Canvas integration\n- State synchronization',
            ),
            (
                'Performance and Deployment',
                'Measure performance, reduce module size, and ship WebAssembly assets efficiently in a production web app.\n\nCore concepts:\n- Profiling boundaries\n- wasm-opt optimization\n- Lazy loading modules\n- Hosting and MIME configuration',
            ),
        ],
    },
    'growth-marketing-101': {
        'video_url': 'https://www.youtube.com/embed/-GBcQ0AGf88',
        'lessons': [
            (
                'Introduction to Growth Marketing',
                'Learn how growth teams combine customer insight, experimentation, and measurement across the full lifecycle.\n\nCore concepts:\n- Growth loops and funnels\n- Acquisition, activation, retention, and referral\n- Experiment velocity\n- Sustainable growth',
            ),
            (
                'Audience and Acquisition Channels',
                'Define useful audience segments and select channels based on intent, economics, and strategic fit.\n\nCore concepts:\n- Ideal customer profiles\n- Organic and paid acquisition\n- Channel-market fit\n- Customer acquisition cost',
            ),
            (
                'Conversion and Activation',
                'Improve the path from first visit to meaningful product value with focused messaging and onboarding.\n\nCore concepts:\n- Landing-page clarity\n- Conversion funnels\n- Activation events\n- Onboarding experiments',
            ),
            (
                'Retention and Lifecycle Marketing',
                'Build habits and customer relationships through relevant messaging, product value, and lifecycle campaigns.\n\nCore concepts:\n- Cohort retention\n- Email lifecycle programs\n- Churn analysis\n- Referral loops',
            ),
            (
                'Analytics and Experimentation',
                'Create a disciplined testing process and make decisions using trustworthy metrics.\n\nCore concepts:\n- Event tracking plans\n- A/B testing\n- Statistical and practical significance\n- Experiment documentation',
            ),
        ],
    },
}


def expand_curricula(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Lesson = apps.get_model('courses', 'Lesson')

    for course_slug, curriculum in CURRICULA.items():
        course = Course.objects.filter(slug=course_slug).first()
        if not course:
            continue

        for order, (title, content) in enumerate(curriculum['lessons'], start=1):
            lesson, _ = Lesson.objects.update_or_create(
                course=course,
                order=order,
                defaults={
                    'title': title,
                    'slug': f'{course_slug}-lesson-{order}',
                    'content': content,
                    'video_url': curriculum['video_url'] if order == 1 else None,
                },
            )
            Lesson.objects.filter(
                course=course,
                slug=f'{course_slug}-lesson-{order}',
            ).exclude(pk=lesson.pk).delete()


def restore_basic_curricula(apps, schema_editor):
    Course = apps.get_model('courses', 'Course')
    Lesson = apps.get_model('courses', 'Lesson')

    for course_slug in CURRICULA:
        course = Course.objects.filter(slug=course_slug).first()
        if not course:
            continue
        Lesson.objects.filter(course=course, order__gt=2).delete()
        Lesson.objects.filter(course=course, order=1).update(
            title='Introduction',
            slug=f'{course_slug}-introduction',
            content=f'Welcome to {course.title}. Learn the core concepts and prepare your development environment.',
        )
        Lesson.objects.filter(course=course, order=2).update(
            title='Core Concepts',
            slug=f'{course_slug}-core-concepts',
            content=f'Explore the essential tools, techniques, and practical workflows used in {course.title}.',
            video_url=None,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_learnerprofile_avatar'),
    ]

    operations = [
        migrations.RunPython(expand_curricula, restore_basic_curricula),
    ]
