*Deck VelVir
      Subroutine VelVir(Cart,Cmem,Stats,Potent,AGd,IAn,AtMass,RtMass,
     $  LPath,LFrag,NFrag,IRT,RT,IDone,ITrpt,dPdT,Scr1,NBond,Neigh,
     $  IBondT,MxBond,TStep,NAtoms,NAt3,MaxStp,NPath,MaxFg,NStat,IStep,
     $  Done,IOut,IPrint,RxnPth,Stop,ReCalc,RxnFwd,TScale,v0,Error,
     $  Crit1,Crit2,ITraj,EFac,GScale,VPrime)
C
C     Take a step using velocity verlet algorithm
C     Also used for damped velocity verlet (DVV) for reaction pathway
C     following (H.P. Hratchian, May 2000)
C
      Implicit Real*8(A-H,O-Z)
      Dimension Cart(NAt3,MaxStp),Cmem(NAt3,MaxStp),Stats(NStat,MaxStp),
     $  AGd(NAt3),IAn(NAtoms),AtMass(NAtoms),RtMass(NAtoms),LPath(*),
     $  LFrag(*),NFrag(20),IRT(20,3),RT(20,6),dPdT(NAt3),Scr1(NAt3,4),
     $  NBond(NAtoms),Neigh(MxBond,NAtoms),IBondT(MxBond,NAtoms),
     $  VPrime(NAt3),XXA(1)
      Logical Done,RxnPth,Stop,TScale,ReCalc,RxnFwd
      Save Zero,Half,XXA
      Data Zero/0.d0/,Half/.5d0/,XXA/0.d0/
C
C     Convert gradients to acceleration terms
C
      Done = .False.
      Call MWeigV(.True.,NAtoms,AGd,RtMass,Scr1)
      Call AScale(NAt3,-GScale,Scr1,dPdT)
C
      Call AMove(NAt3,Cmem(1,IStep),VPrime)
C
C     Finish up previous step (IStep) and test for convergence
C
      if(IStep.ge.3) then
        TStp = TStep
        Call ACasB(NAt3,Cmem(1,IStep),dPdT,Cmem(1,IStep),Half*TStp)
      endif
C
C     If RxnPth is .True. then Damped Velocity Verlet is used to
C     follow the reaction pathway.
C
      DDel = Zero
C DBLs
C Calculate equipartition energy, 1/2 kb T for each nuclear DOF in
C hartree.  Compare that to current Ekin, find difference, and scale
C current cmem uniformly to make up the difference.
C
      If(Mod(IStep,IgtIOP(199)).eq.0) then
        boltz= 3.167D-6 
        atms3 = gfloat(NAtoms)*3.d0
        temp = gfloat(IgtIOP(198))
        thermKE = boltz*temp*(atms3-3)/2.d0
        write(*,*)'Thermal Energy',thermKE
        EKinT = Half*Efac*Sprod(NAt3,Cmem(1,IStep),Cmem(1,IStep))
        Ediff = thermKE - EKinT
        Escale = GSqrt((EkinT+Ediff)/EkinT)
        Call AScale(NAt3,Escale,Cmem(1,IStep),Cmem(1,IStep))
        Write(*,*)'New/old kinetic energy ',Half*Efac*Sprod(NAt3,Cmem(1,
     $    IStep),Cmem(1,IStep)),EKinT
      endIf 
C
C DBLe
C
C     Compute some useful statistics
C
      Call TjStat(IOut,IPrint,Stats,Cart(1,IStep-1),Cart(1,IStep),
     $  Cmem(1,IStep),TStp,Potent,DDel,AGd,XXA,AtMass,RtMass,Scr1,
     $  NAtoms,NAt3,IStep,ITraj,Zero,3,NStat,EFac,.False.,RxnPth,RxnFwd)
C
C     For standard velocity verlet, check to see if trajectory
C     is finished
C
      Call FTest(IOut,IPrint,IDone,Cart(1,IStep),Cmem(1,IStep),AGd,Done,
     $  NAtoms,NAt3,LPath,LFrag,NFrag,ITrpt,Scr1,Scr1(1,2),IAn,AtMass,
     $  RtMass,IRT,RT,NBond,Neigh,IBondT,MxBond,MaxStp,IStep,NPath,
     $  MaxFg,RxnPth,Stop,Crit1,Crit2)
C
C     Predict the next step (IStep --> IStep+1)
C
      if(.not.Done) then
        Call ACasB(NAt3,Cmem(1,IStep),dPdT,Cmem(1,IStep+1),Half*TStep)
        Call MWeigV(.True.,NAtoms,Cmem(1,IStep+1),RtMass,Scr1)
        Call ACasB(NAt3,Cart(1,IStep),Scr1,Cart(1,IStep+1),TStep)
C
C       Compute some more vital statistics
C       (Becareful since, Cmem is not completed yet)
C
        Call TjStat(IOut,IPrint,Stats,Cart(1,IStep),Cart(1,IStep+1),
     $    Cmem(1,IStep+1),TStep,Potent,Zero,AGd,XXA,AtMass,RtMass,Scr1,
     $    NAtoms,NAt3,IStep+1,ITraj,Zero,4,NStat,EFac,.False.,RxnPth,
     $    RxnFwd)
        endif
      Return
      End
